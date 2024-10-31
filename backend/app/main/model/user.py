import datetime
from app.main import flask_bcrypt
from app.main.config import key
from app.main.util.database import db_get_cursor, UniqueViolation
import jwt


class User(object):
    class AlreadyExistsError(Exception):
        pass

    class BadInputError(Exception):
        pass

    class NotFoundError(Exception):
        pass

    class TokenBlacklistedError(Exception):
        pass

    class TokenExpiredError(Exception):
        pass

    class TokenInvalidError(Exception):
        pass

    # TODO: Type hint for `created_at`?
    def __init__(
        self,
        id: int,
        email: str,
        username: str,
        password_hash: str,
        created_at,
        person_id: int,
    ):
        self._id = id
        self._email = email
        self._username = username
        self._password_hash = password_hash
        self._created_at = created_at
        self._person_id = person_id

    @staticmethod
    def new_user(email: str, username: str, password: str) -> "User":
        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO user (email, username, password_hash)
                        VALUES (%s, %s, %s);
                        """,
                    (email, username, User.hash_password(password)),
                )
        except UniqueViolation:
            raise User.AlreadyExistsError
        except NotNullViolation:
            raise User.BadInputError
        return User.get_by_email(email)

    @staticmethod
    def get_by_email(email: str) -> "User":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s;", email)
            result = cur.fetchone()

        try:
            return User(*result)
        except TypeError:
            raise User.NotFoundError

    @staticmethod
    def get_by_id(id: int) -> "User":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", id)
            result = cur.fetchone()

        try:
            return User(*result)
        except TypeError:
            raise User.NotFoundError

    @staticmethod
    def get_by_login(email: str, password: str) -> "User":
        user = User.get_by_email(email)
        if not user.check_password(password):
            raise User.NotFoundError
        return user

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        raise AttributeError("id: read-only field")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        raise AttributeError("email: read-only field")

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str):
        if self.check_password(password):
            raise AttributeError("password: cannot set same password")

        self._password_hash = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )
        self._update()

    @property
    def created_at(self):
        return self._created_at

    @property
    def person_id(self) -> int:
        return self._person_id

    @person_id.setter
    def person_id(self, person_id: int):
        if self._person_id is not None:
            raise AttributeError("person_id: read-only field")

        self._person_id = person_id
        self._update()

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self._password_hash, password)

    def _update(self):
        with db_get_cursor() as cur:
            cur.execute(
                """
                        UPDATE user
                        SET password_hash = %s,
                            person_id = %s
                        WHERE id = %s
                        """,
                (self.password_hash, self.person_id, self.id),
            )

    def encode_auth_token(self) -> bytes:
        payload = {
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=1, seconds=5),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "sub": self.id,
        }
        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decode_auth_token(auth_token: str) -> "User":
        try:
            payload = jwt.decode(auth_token, key)
        except jwt.ExpiredSignatureError:
            raise User.TokenExpiredError
        except jwt.InvalidTokenError:
            raise User.TokenInvalidError

        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM blacklist_token WHERE token = %s", (auth_token,))
            is_blacklisted = cur.fetchone() is not None

        if is_blacklisted:
            raise User.TokenBlacklistedError
        else:
            return User.get_by_id(payload["sub"])
