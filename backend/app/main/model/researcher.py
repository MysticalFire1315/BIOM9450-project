from typing import Dict, List

from app.main.util.database import db_get_cursor
from app.main.util.exceptions.errors import NotFoundError


class Researcher(object):
    def __init__(
        self,
        id: int,
        title: str,
        phone: str,
        email: str,
        area_of_research: str,
        people_id: int,
    ):
        self._id = id
        self._title = title
        self._phone = phone
        self._email = email
        self._area_of_research = area_of_research
        self._people_id = people_id

    @staticmethod
    def get_by_people_id(people_id: int) -> "Researcher":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM researchers WHERE people_id = %s;", (people_id,))
            result = cur.fetchone()

        try:
            return Researcher(*result)
        except TypeError:
            raise NotFoundError("Researcher not found")

    @staticmethod
    def get_all() -> List["Researcher"]:
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM researchers;")
            result = cur.fetchall()

        return [Researcher(*r) for r in result]

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def email(self) -> str:
        return self._email

    @property
    def area_of_research(self) -> str:
        return self._area_of_research

    @property
    def people_id(self) -> int:
        return self._people_id

    @property
    def positions(self) -> List[Dict[str, str]]:
        with db_get_cursor() as cur:
            cur.execute(
                """
                SELECT title, organization, start_date, end_date FROM researcher_positions
                WHERE researcher_id = %s;
                """,
                (self.id,),
            )
            result = cur.fetchall()

        return [
            {
                "title": r[0],
                "organization": r[1],
                "start_date": r[2],
                "end_date": r[3],
            }
            for r in result
        ]
