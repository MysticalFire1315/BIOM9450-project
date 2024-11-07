from typing import Dict, Tuple

from app.main.service.patient_service import create_patient, get_profile
from app.main.util.dto import PatientDto
from app.main.util.decorator import require_logged_in_as
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
        return get_profile(person)