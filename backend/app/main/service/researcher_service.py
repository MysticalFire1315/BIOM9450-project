from app.main.model.person import Person
from app.main.model.researcher import Researcher


def get_profile(people_id: int) -> Researcher:
    """Retrieves the profile of a researcher by their people ID.

    Args:
        people_id (int): The people ID of the researcher to retrieve.

    Returns:
        Researcher: The Researcher object with the associated person details.
    """

    x = Researcher.get_by_people_id(people_id)
    x.person = Person.get_by_id(people_id)
    return x


def get_all_researchers():
    """Retrieves all researchers and their associated person details.

    Returns:
        List[Person]: A list of Person objects representing all researchers.
    """

    return [Person.get_by_id(x.people_id) for x in Researcher.get_all()]
