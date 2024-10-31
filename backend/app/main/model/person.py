from app.main.util.database import db_get_cursor
from app.main.model.user import User
from datetime import datetime
from enum import Enum

class Sex(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    @staticmethod
    def from_str(string: str):
        for x in Sex:
            if x.value == string:
                return x
        raise AttributeError(f'{string} does not exist')

class Role(Enum):
    PATIENT = 'patient'
    ONCOLOGIST = 'oncologist'
    RESEARCHER = 'researcher'

    @staticmethod
    def from_str(string: str):
        for x in Role:
            if x.value == string:
                return x
        raise AttributeError(f'{string} does not exist')


class Person(object):
    def __init__(
        self, firstname: str, lastname: str, date_of_birth: datetime, sex: Sex | str, role: Role | str
    ):
        self._id = id
        self._firstname = firstname
        self._lastname = lastname
        self._date_of_birth = date_of_birth
        self._sex = type(sex) is str ? Sex.from_str(sex) : sex
        self._role = type(role) is str ? Role.from_str(role) : role

    @staticmethod
    def new_person(firstname: str, lastname: str, date_of_birth: datetime, sex: Sex, role: Role):
        with db_get_cursor() as cur:
            cur.execute(
                "INSERT INTO person (firstname, lastname, date_of_birth, sex, role) VALUES (%s, %s, %s, %s, %s)",
                (firstname, lastname, date_of_birth, sex.value, role.value),
            )
        return Person.get_person(firstname, lastname, date_of_birth, sex)

    @staticmethod
    def get_person(firstname: str, lastname: str, date_of_birth: datetime, sex: Sex, role: Role):
        with db_get_cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM person
                WHERE firstname = %s
                    AND lastname = %s
                    AND date_of_birth = %s
                    AND sex = %s
                """,
                (firstname, lastname, date_of_birth, sex.value),
            )
            result = cur.fetchone()

        try:
            return Person(*result)
        except TypeError:
            raise Person.NotFoundError

    @staticmethod
    def get_by_user_id(user_id: int):
        try:
            user = User.get_by_id(user_id)
        except User.NotFoundError:
            raise Person.NotFoundError

        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM person WHERE id = %s;", (user.person_id,))
            result = cur.fetchone()

        try:
            return Person(*result)
        except TypeError:
            raise Person.NotFoundError

    @property
    def id(self) -> int:
        return self._id

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, value: str):
        self._firstname = value
        self._update()

    @property
    def lastname(self) -> str:
        return self._lastname

    @lastname.setter
    def lastname(self, value: str):
        self._lastname = value
        self._update()

    @property
    def date_of_birth(self) -> datetime:
        return self._date_of_birth

    @property
    def sex(self) -> Sex:
        return self._sex

    @property
    def role(self) -> Role:
        # For now role cannot be updated - possible idea for future
        return self._role

    def _update(self):
        with db_get_cursor() as cur:
            cur.execute(
                """
                UPDATE person
                SET firstname = %s,
                    lastname = %s
                WHERE id = %s
                """,
                (self.firstname, self.lastname, self.id),
            )
