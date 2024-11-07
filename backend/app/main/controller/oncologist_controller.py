from typing import Dict, Tuple

from app.main.service.oncologist_service import get_profile
from app.main.util.decorator import require_logged_in_as
from app.main.util.dto import OncologistDto
from flask_restx import Resource

api = OncologistDto.api

@api.route("/profile")
class ProfileAPI(Resource):
    @api.doc("get the oncologist's profile")
    @api.response(200, "Oncologist profile")
    @api.marshal_with(OncologistDto.oncologist_profile, envelope="data")
    @require_logged_in_as(oncologist=True, throughpass=True)
    def get(self, person):
        return get_profile(person)