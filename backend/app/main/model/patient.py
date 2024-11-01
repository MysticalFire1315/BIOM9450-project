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
        person_id: int = None,
    ):
        self._id = id
        self._photo = photo
        self._address = address
        self._country = country
        self._emergency_contact_name = emergency_contact_name
        self._emergency_contact_phone = emergency_contact_phone
        self._created_at = created_at
        self._updated_at = updated_at
        self._person_id = person_id

    @staticmethod
    def new_patient(person_id: int, photo: bytes = None,
        address: str = None,
        country: str = None,
        emergency_contact_name: str = None,
        emergency_contact_phone: str = None) -> "Patient":
        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO patients (photo, address, country, emergency_contact_name, emergency_contact_phone, person_id)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (photo, address, country, emergency_contact_name, emergency_contact_phone, person_id)
                )
        except UniqueViolation:
            raise AlreadyExistsError('Patient already exists')
        except NotNullViolation:
            raise BadInputError('Bad input')
        return Patient.get_by_person_id(person_id)

    @staticmethod
    def get_by_person_id(person_id: int) -> "Patient":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE person_id = %s;", (person_id,))
            result = cur.fetchone()

        try:
            return Patient(*result)
        except TypeError:
            raise NotFoundError('Patient not found')
