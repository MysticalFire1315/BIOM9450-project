import traceback
from flask import current_app
import datetime

from app.main.util.database import db_get_cursor, UniqueViolation, NotNullViolation
from app.main.util.exceptions.errors import NotFoundError, BadInputError

class Patient(object):
    def __init__(
        self,
        id: int,
        photo: bytes = None,
        address: str = None,
        country: str = None,
        emergency_contact_name: str = None,
        emergency_contact_phone: str = None,
        created_at: datetime.datetime = None,
        updated_at: datetime.datetime = None,
        people_id: int = None,
    ):
        self._id = id
        self._photo = photo
        self._address = address
        self._country = country
        self._emergency_contact_name = emergency_contact_name
        self._emergency_contact_phone = emergency_contact_phone
        self._created_at = created_at
        self._updated_at = updated_at
        self._people_id = people_id

    @staticmethod
    def new_patient(people_id: int, photo: bytes = None,
        address: str = None,
        country: str = None,
        emergency_contact_name: str = None,
        emergency_contact_phone: str = None) -> "Patient":
        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO patients (photo, address, country, emergency_contact_name, emergency_contact_phone, people_id)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (photo, address, country, emergency_contact_name, emergency_contact_phone, people_id)
                )
        except UniqueViolation:
            raise AlreadyExistsError('Patient already exists')
        except NotNullViolation:
            raise BadInputError('Bad input')
        return Patient.get_by_people_id(people_id)

    @staticmethod
    def get_by_people_id(people_id: int) -> "Patient":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE people_id = %s;", (people_id,))
            result = cur.fetchone()

        try:
            return Patient(*result)
        except TypeError:
            raise NotFoundError('Patient not found')

    @property
    def id(self) -> int:
        return self._id

    @property
    def photo(self) -> bytes:
        return self._photo

    @property
    def address(self) -> str:
        return self._address

    @property
    def country(self) -> str:
        return self._country

    @property
    def emergency_contact_name(self) -> str:
        return self._emergency_contact_name

    @property
    def emergency_contact_phone(self) -> str:
        return self._emergency_contact_phone

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime.datetime:
        return self._updated_at

    @property
    def people_id(self) -> int:
        return self._people_id
