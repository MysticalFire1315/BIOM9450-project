import traceback
from flask import current_app
import datetime

from app.main.util.database import db_get_cursor, UniqueViolation, NotNullViolation
from app.main.util.exceptions.errors import NotFoundError, BadInputError

class Oncologist(object):
    def __init__(
        self,
        id: int,
        people_id: int,
    ):
        self._id = id
        self._people_id = people_id

    @staticmethod
    def new_oncologist(people_id: int) -> "Oncologist":
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
