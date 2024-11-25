from datetime import datetime
from enum import Enum
from typing import Union

from app.main.util.database import NotNullViolation, db_get_cursor
from app.main.util.exceptions.errors import BadInputError, NotFoundError


class Sex(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

    @staticmethod
    def from_str(string: str):
        for x in Sex:
            if x.value == string:
                return x
        raise BadInputError(f"{string} does not exist")


class Person(object):
    """Representation of a person."""

    def __init__(
        self,
        id: int,
        firstname: str,
        lastname: str,
        date_of_birth: datetime,
        sex: Union[Sex, str],
    ):
        self._id = id
        self._firstname = firstname
        self._lastname = lastname
        self._date_of_birth = date_of_birth
        self._sex = Sex.from_str(sex) if isinstance(sex, str) else sex

    @staticmethod
    def new_person(
        firstname: str, lastname: str, date_of_birth: datetime, sex: Sex
    ) -> "Person":
        try:
            with db_get_cursor() as cur:
                cur.execute(
                    "INSERT INTO people (firstname, lastname, date_of_birth, sex) VALUES (%s, %s, %s, %s);",
                    (firstname, lastname, date_of_birth, sex.value),
                )
        except NotNullViolation:
            raise BadInputError("Bad input")
        return Person.get_by_details(firstname, lastname, date_of_birth, sex)

    @staticmethod
    def get_by_details(
        firstname: str, lastname: str, date_of_birth: datetime, sex: Sex
    ) -> "Person":
        with db_get_cursor() as cur:
            cur.execute(
                """;
                SELECT *
                FROM people
                WHERE firstname = %s
                    AND lastname = %s
                    AND date_of_birth = %s
                    AND sex = %s;
                """,
                (firstname, lastname, date_of_birth, sex.value),
            )
            result = cur.fetchone()

        try:
            return Person(*result)
        except TypeError:
            raise NotFoundError("Person not found")

    @staticmethod
    def get_by_id(id: int) -> "Person":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM people WHERE id = %s;", (id,))
            result = cur.fetchone()

        try:
            return Person(*result)
        except TypeError:
            raise NotFoundError("Person not found")

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

    def _update(self):
        with db_get_cursor() as cur:
            cur.execute(
                """
                UPDATE people
                SET firstname = %s,
                    lastname = %s
                WHERE id = %s;
                """,
                (self.firstname, self.lastname, self.id),
            )

    def delete(self):
        with db_get_cursor() as cur:
            cur.execute("DELETE FROM people WHERE id = %s", (self.id,))
