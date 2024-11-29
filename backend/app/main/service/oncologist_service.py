from app.main.model.oncologist import Oncologist
from app.main.model.person import Person


def get_all_oncologists():
    """Retrieves all oncologists and their associated person details.

    Returns:
        List[Person]: A list of Person objects representing all oncologists.
    """

    return [Person.get_by_id(x.people_id) for x in Oncologist.get_all()]


def get_profile(id: int):
    """Retrieves the profile of an oncologist by their people ID.

    Args:
        id (int): The people ID of the oncologist to retrieve.

    Returns:
        Oncologist: The Oncologist object with the associated person details.
    """

    x = Oncologist.get_by_people_id(id)
    x.person = Person.get_by_id(id)
    return x
