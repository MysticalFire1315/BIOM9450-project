from typing import Dict, Tuple

from app.main.service.patient_service import create_patient, get_profile, get_all_patients, mutation_upload, get_mutations
from app.main.util.dto import PatientDto, PersonDto
from app.main.util.decorator import require_logged_in_as
from app.main.util.exceptions.errors import BadInputError
from flask import request
from flask_restx import Resource

api = PatientDto.api

@api.route("/create")
class CreateAPI(Resource):
    @api.doc("create a new patient profile")
    @require_logged_in_as(oncologist=True, researcher=True)
    @api.expect(PatientDto.patient_profile, validate=True)
    @api.response(201, "Patient successfully created.")
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return create_patient(post_data)

@api.route("/profile")
class ProfileAPI(Resource):
    @api.doc("get the patient's profile")
    @api.response(200, "Patient profile")
    @api.marshal_with(PatientDto.patient_profile, envelope="data")
    @require_logged_in_as(patient=True, throughpass=True)
    def get(self, person):
        return get_profile(person.id)

@api.route("/profile/<id>")
class ProfileAPI(Resource):
    @api.doc("get the patient's profile")
    @api.response(200, "patient profile")
    @api.marshal_with(PatientDto.patient_profile, envelope="data")
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self, id):
        return get_profile(id)

@api.route("/profile/<id>/mutations")
class ProfileMutationsAPI(Resource):
    @api.doc("get the patient's profile")
    @api.response(200, "patient profile")
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self, id):
        return get_mutations(id)

@api.route("/list")
class ListAPI(Resource):
    @api.doc("list of patients")
    @api.marshal_list_with(PersonDto.person_profile, envelope="data")
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self):
        return get_all_patients()

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type='file', required=True, help='VCF file to upload')
upload_parser.add_argument('patient_id', location='form', type=int, required=False, help='Patient ID')
upload_parser.add_argument('people_id', location='form', type=int, required=False, help='People ID')

@api.route("/mutation/upload")
class MutationUploadAPI(Resource):
    @api.doc("upload a mutation file")
    @api.expect(upload_parser)
    @require_logged_in_as(oncologist=True, researcher=True)
    def post(self):
        args = request.form
        patient_id = args.get('patient_id')
        people_id = args.get('people_id')
        file = request.files.get('file')

        if not file:
            raise BadInputError("No file part in the request")
        elif not patient_id and not people_id:
            raise BadInputError("Either patient_id or people_id must be provided")
        elif file.filename == '':
            raise BadInputError("No file selected")

        return mutation_upload(patient_id, people_id, file)
