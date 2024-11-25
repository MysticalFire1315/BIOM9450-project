from typing import Dict, Tuple, Optional
import tempfile
import pysam
import os

from app.main.model.patient import Patient
from app.main.model.person import Person, Sex
from app.main.util.exceptions.errors import CustomError

def create_patient(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    person_data = data.get("person")
    person = Person.new_person(
        person_data.get("firstname"),
        person_data.get("lastname"),
        person_data.get("date_of_birth"),
        Sex.from_str(person_data.get("sex"))
    )

    try:
        p = Patient.new_patient(
            person.id,
            data.get("photo"),
            data.get("address"),
            data.get("country"),
            data.get("emergency_contact_name"),
            data.get("emergency_contact_phone")
        )
        return {"status": "success", "message": "Successfully created", "id": p.people_id}, 201
    except CustomError as error:
        person.delete()
        raise error

def get_profile(id: int):
    x = Patient.get_by_people_id(id)
    x.person = Person.get_by_id(id)
    return x

def get_mutations(id: int):
    x = Patient.get_by_people_id(id)
    return {"status": "success", "mutations": x.get_mutations()}, 200

def get_all_patients():
    return Patient.get_all()

def mutation_upload(patient_id: Optional[int], people_id: Optional[int], file):
    gene_names = set()

    try:
        # Store the uploaded file in a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf") as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        # Open the temporary file with pysam
        with pysam.VariantFile(temp_file_path) as vcf:
            for record in vcf.fetch():
                # Extract gene names from INFO fields
                if 'GENE' in record.info:
                    gene_names.add(record.info['GENE'])
                elif 'ANN' in record.info:
                    for ann in record.info['ANN']:
                        gene_name = ann.split('|')[2]
                        gene_names.add(gene_name)
    except Exception as e:
        raise e
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    if patient_id:
        patient = Patient.get_by_id(patient_id)
    else:
        patient = Patient.get_by_people_id(people_id)

    patient.link_mutations(list(gene_names))

    return {"status": "success", "genes": list(gene_names)}, 201
