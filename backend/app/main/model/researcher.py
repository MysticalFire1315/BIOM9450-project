import traceback
from flask import current_app
import datetime
from typing import List

from app.main.util.database import db_get_cursor, UniqueViolation, NotNullViolation
from app.main.util.exceptions.errors import NotFoundError, BadInputError
from app.main.model.person import Person

class Researcher(object):
    def __init__(
        self,
        id: int,
        people_id: int,
    ):
        self._id = id
        self._people_id = people_id

    @staticmethod
    def new_researcher(people_id: int) -> "Researcher":
        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO researchers (people_id)
                    VALUES (%s);
                    """,
                    (people_id)
                )
        except UniqueViolation:
            raise AlreadyExistsError('Researcher already exists')
        except NotNullViolation:
            raise BadInputError('Bad input')
        return Researcher.get_by_people_id(people_id)

    @staticmethod
    def get_by_people_id(people_id: int) -> "Researcher":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM researchers WHERE people_id = %s;", (people_id,))
            result = cur.fetchone()

        try:
            return Researcher(*result)
        except TypeError:
            raise NotFoundError('Researcher not found')

    @staticmethod
    def get_all() -> List[Person]:
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM researchers;")
            result = cur.fetchall()

        return [Person.get_by_id(Researcher(*r).people_id) for r in result]

    @property
    def id(self) -> int:
        return self._id

    @property
    def people_id(self) -> int:
        return self._people_id