import datetime
from typing import List

from psycopg2.extras import execute_values

from app.main.model.ml import MLModel
from app.main.model.person import Person
from app.main.util.database import NotNullViolation, UniqueViolation, db_get_cursor
from app.main.util.exceptions.errors import (
    AlreadyExistsError,
    BadInputError,
    NotFoundError,
)


class Patient(object):
    """Representation of a patient."""

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
    def new_patient(
        people_id: int,
        photo: bytes = None,
        address: str = None,
        country: str = None,
        emergency_contact_name: str = None,
        emergency_contact_phone: str = None,
    ) -> "Patient":
        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO patients (photo, address, country, emergency_contact_name, emergency_contact_phone, people_id)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        photo,
                        address,
                        country,
                        emergency_contact_name,
                        emergency_contact_phone,
                        people_id,
                    ),
                )
        except UniqueViolation:
            raise AlreadyExistsError("Patient already exists")
        except NotNullViolation:
            raise BadInputError("Bad input")
        return Patient.get_by_people_id(people_id)

    @staticmethod
    def get_by_id(patient_id: int) -> "Patient":
        """Retrieves a patient from the database by their ID.

        Args:
            patient_id (int): The ID of the patient to retrieve.

        Returns:
            Patient: The retrieved Patient object.

        Raises:
            NotFoundError: If no patient with the given ID exists.
        """

        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE id = %s;", (patient_id,))
            result = cur.fetchone()

        if result:
            return Patient(*result)
        else:
            raise NotFoundError("Patient not found")

    @staticmethod
    def get_by_people_id(people_id: int) -> "Patient":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE people_id = %s;", (people_id,))
            result = cur.fetchone()

        try:
            return Patient(*result)
        except TypeError:
            raise NotFoundError("Patient not found")

    @staticmethod
    def get_all() -> List["Patient"]:
        """Retrieves all patients from the database.

        Returns:
            List[Patient]: A list of all Patient objects.
        """

        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM patients;")
            results = cur.fetchall()

        return [Patient(*result) for result in results]

    def save(self):
        """Saves the current state of the patient to the database."""

        with db_get_cursor() as cur:
            cur.execute(
                """
                UPDATE patients
                SET photo = %s, address = %s, country = %s, emergency_contact_name = %s,
                    emergency_contact_phone = %s, created_at = %s, updated_at = %s, people_id = %s
                WHERE id = %s;
                """,
                (
                    self._photo,
                    self._address,
                    self._country,
                    self._emergency_contact_name,
                    self._emergency_contact_phone,
                    self._created_at,
                    self._updated_at,
                    self._people_id,
                    self._id,
                ),
            )

    def delete(self):
        """Deletes the patient from the database."""
        with db_get_cursor() as cur:
            cur.execute("DELETE FROM patients WHERE id = %s;", (self._id,))

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

    def link_mutations(self, mutations_list: List[str]):
        """Links a list of mutations to the patient in the database.

        Args:
            mutations_list (List[str]): A list of mutation names to be linked to the patient.
        """

        feat_dict = MLModel.update_feat_dict(mutations_list)
        current_mutations = set(self.get_mutations())
        to_execute = [
            (self.id, feat_dict[m])
            for m in mutations_list
            if m not in current_mutations
        ]
        with db_get_cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO patient_mutations (patient_id, feat_id) VALUES %s;",
                to_execute,
            )

    def get_mutations(self) -> List[str]:
        """Retrieves the list of mutations linked to the patient from the database.

        Returns:
            List[str]: A list of mutation names linked to the patient.
        """

        feat_dict = {v: k for k, v in MLModel.get_feat_dict().items()}
        with db_get_cursor() as cur:
            cur.execute(
                "SELECT feat_id FROM patient_mutations WHERE patient_id = %s;",
                (self.id,),
            )
            result = cur.fetchall()

        return [feat_dict[i[0]] for i in result]
