from typing import List

from app.main.util.database import db_get_cursor
from app.main.util.exceptions.errors import NotFoundError


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
    def get_by_people_id(people_id: int) -> "Oncologist":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM oncologists WHERE people_id = %s;", (people_id,))
            result = cur.fetchone()

        try:
            return Oncologist(*result)
        except TypeError:
            raise NotFoundError("Oncologist not found")

    @staticmethod
    def get_all() -> List["Oncologist"]:
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM oncologists;")
            result = cur.fetchall()

        return [Oncologist(*r) for r in result]

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
            cur.execute(
                """
                SELECT hospital FROM oncologist_affiliations
                WHERE oncologist_id = %s;
                """,
                (self.id,),
            )
            return [i for j in cur.fetchall() for i in j]
