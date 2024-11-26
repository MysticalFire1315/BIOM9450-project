import logging

import requests

from app.main.model.patient import Patient
from app.main.util.database import db_get_cursor
from app.main.util.exceptions.errors import NotFoundError


def get_all_mutations():
    """Retrieves all mutation names from the database.

    Returns:
        List[str]: A list of all mutation names.
    """

    with db_get_cursor() as cur:
        cur.execute("SELECT name FROM features;")
        result = cur.fetchall()
    return [row[0] for row in result]


def get_mutation(name: str):
    """Retrieves mutation data from COSMIC and the database.

    Args:
        name (str): The name of the mutation to retrieve.

    Returns:
        Dict[str, Union[List[Dict[str, str]], List[int]]]: A dictionary containing COSMIC data and patient IDs.

    Raises:
        NotFoundError: If the mutation is not found in COSMIC or the database.
    """

    # Get mutation data from COSMIC
    url = "https://clinicaltables.nlm.nih.gov/api/cosmic/v4/search"
    params = {"terms": name, "df": "MutationID,GeneName,PrimarySite"}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        logging.getLogger("errors").warning(
            f"GET {response.url} failed with status {response.status_code}"
        )
        raise NotFoundError("Mutation not found")

    data = response.json()
    if not data:
        raise NotFoundError("Mutation not found")

    output = {
        "COSMIC_data": [
            {
                "mutation_id": mutation_id,
                "gene_name": gene_name,
                "primary_site": primary_site,
            }
            for mutation_id, gene_name, primary_site in sorted(
                data[-1], key=lambda x: x[0]
            )
        ],
        "patients": [],
    }

    with db_get_cursor() as cur:
        cur.execute(
            """
            SELECT pm.patient_id
            FROM features f
                JOIN patient_mutations pm ON f.id = pm.feat_id
            WHERE f.name = %s;
        """,
            (name,),
        )
        result = cur.fetchall()

    if result:
        output["patients"] = [Patient.get_by_id(r[0]).people_id for r in result]

    return output
