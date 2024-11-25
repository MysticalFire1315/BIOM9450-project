from flask_restx import Resource

from app.main.service.researcher_service import get_all_researchers, get_profile
from app.main.util.decorator import require_logged_in_as
from app.main.util.dto import PersonDto, ResearcherDto

api = ResearcherDto.api


@api.route("/profile")
class ProfileAPI(Resource):
    @api.doc("get the researcher's profile")
    @api.marshal_with(ResearcherDto.researcher_profile, envelope="data")
    @require_logged_in_as(researcher=True, throughpass=True)
    def get(self, person):
        return get_profile(person.id)


@api.route("/profile/<id>")
class ProfileIdAPI(Resource):
    @api.doc("get the researcher's profile")
    @api.marshal_with(ResearcherDto.researcher_profile, envelope="data")
    def get(self, id):
        return get_profile(id)


@api.route("/list")
class ListAPI(Resource):
    @api.doc("list of researchers")
    @api.marshal_list_with(PersonDto.person_profile, envelope="data")
    def get(self):
        return get_all_researchers()
