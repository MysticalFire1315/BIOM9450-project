import datetime
from typing import Union

import jwt

from app.main import flask_bcrypt
from app.main.config import key
from app.main.util.database import NotNullViolation, UniqueViolation, db_get_cursor
from app.main.util.exceptions.errors import (
    AlreadyExistsError,
    BadInputError,
    NotFoundError,
    TokenInvalidError,
)


class User(object):
    def __init__(
        self,
        id: int,
        email: str,
        username: str,
        password_hash: str,
        created_at: datetime.datetime,
        people_id: int,
    ):
        self._id = id
        self._email = email
        self._username = username
        self._password_hash = password_hash
        self._created_at = created_at
        self._people_id = people_id

    @staticmethod
    def new_user(email: str, username: str, password: str) -> "User":
        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (email, username, password_hash)
                    VALUES (%s, %s, %s);
                    """,
                    (email, username, User.hash_password(password)),
                )
        except UniqueViolation:
            raise AlreadyExistsError("User already exists")
        except NotNullViolation:
            raise BadInputError("Bad input")
        return User.get_by_email(email)

    @staticmethod
    def get_by_email(email: str) -> "User":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
            result = cur.fetchone()

        try:
            return User(*result)
        except TypeError:
            raise NotFoundError("User not found")

    @staticmethod
    def get_by_id(id: int) -> "User":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
            result = cur.fetchone()

        try:
            return User(*result)
        except TypeError:
            raise NotFoundError("User not found")

    @staticmethod
    def get_by_login(email: str, password: str) -> "User":
        user = User.get_by_email(email)
        if not user.check_password(password):
            raise NotFoundError("User not found")
        return user

    @property
    def id(self) -> int:
        return self._id

    @property
    def email(self) -> str:
        return self._email

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        raise BadInputError("password: write-only field")

    @password.setter
    def password(self, password: str):
        if self.check_password(password):
            raise BadInputError("password: cannot set same password")

        self._password_hash = User.hash_password(password)
        self._update()

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def people_id(self) -> Union[int, None]:
        return self._people_id

    @people_id.setter
    def people_id(self, people_id: int):
        if self._people_id is not None:
            raise BadInputError("people_id: read-only field")

        self._people_id = people_id
        self._update()

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self._password_hash, password)

    def _update(self):
        with db_get_cursor() as cur:
            cur.execute(
                """
                        UPDATE users
                        SET password_hash = %s,
                            people_id = %s
                        WHERE id = %s;
                        """,
                (self._password_hash, self._people_id, self._id),
            )

    @staticmethod
    def hash_password(password: str) -> str:
        return flask_bcrypt.generate_password_hash(password).decode("utf-8")

    def encode_auth_token(self) -> bytes:
        payload = {
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=1, seconds=5),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "sub": str(self.id),
        }
        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decode_auth_token(auth_token: str) -> "User":
        try:
            payload = jwt.decode(auth_token, key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise TokenInvalidError("Token expired")
        except jwt.InvalidTokenError:
            raise TokenInvalidError("Token invalid")

        with db_get_cursor() as cur:
            cur.execute(
                "SELECT * FROM blacklist_tokens WHERE token = %s", (auth_token,)
            )
            is_blacklisted = cur.fetchone() is not None

        if is_blacklisted:
            raise TokenInvalidError("Token expired")
        else:
            return User.get_by_id(int(payload["sub"]))
