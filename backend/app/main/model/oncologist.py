import traceback
from flask import current_app
import datetime
from typing import List

from app.main.util.database import db_get_cursor, UniqueViolation, NotNullViolation
from app.main.util.exceptions.errors import NotFoundError, BadInputError
from app.main.model.person import Person

class Oncologist(object):
    def __init__(
        self,
        id: int,
        specialization: str,
        phone: str,
        email: str,
        people_id: int,
    ):
        self._id = id
        self._specialization = specialization
        self._phone = phone
        self._email = email
        self._people_id = people_id

    @staticmethod
    def new_oncologist(people_id: int) -> "Oncologist":
        # TODO
        raise NotImplementedError

        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO oncologists (people_id)
                    VALUES (%s);
                    """,
                    (people_id)
                )
        except UniqueViolation:
            raise AlreadyExistsError('Oncologist already exists')
        except NotNullViolation:
            raise BadInputError('Bad input')
        return Oncologist.get_by_people_id(people_id)

    @staticmethod
    def get_by_people_id(people_id: int) -> "Oncologist":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM oncologists WHERE people_id = %s;", (people_id,))
            result = cur.fetchone()

        try:
            return Oncologist(*result)
        except TypeError:
            raise NotFoundError('Oncologist not found')

    @staticmethod
    def get_all() -> List[Person]:
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM oncologists;")
            result = cur.fetchall()

        return [Person.get_by_id(Oncologist(*r).people_id) for r in result]

    @property
    def id(self) -> int:
        return self._id

    @property
    def specialization(self) -> str:
        return self._specialization

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def email(self) -> str:
        return self._email

    @property
    def people_id(self) -> int:
        return self._people_id

    @property
    def affiliations(self) -> List[str]:
        with db_get_cursor() as cur:
            cur.execute("""
                SELECT hospital FROM oncologist_affiliations
                WHERE id = %s;
                """, (self.id,))
            return [i for j in cur.fetchall() for i in j]
