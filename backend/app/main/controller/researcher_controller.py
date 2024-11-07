from typing import Dict, Tuple

from app.main.service.researcher_service import get_profile
from app.main.util.decorator import require_logged_in_as
from app.main.util.dto import ResearcherDto
from flask_restx import Resource

api = ResearcherDto.api

@api.route("/profile")
class ProfileAPI(Resource):
    @api.doc("get the researcher's profile")
    @api.response(200, "Researcher profile")
    @api.marshal_with(ResearcherDto.researcher_profile, envelope="data")
    @require_logged_in_as(researcher=True, throughpass=True)
    def get(self, person):
        return get_profile(person)