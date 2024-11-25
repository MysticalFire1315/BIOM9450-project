from flask_restx import Resource

from app.main.service.oncologist_service import get_all_oncologists, get_profile
from app.main.util.decorator import require_logged_in_as
from app.main.util.dto import OncologistDto, PersonDto

api = OncologistDto.api


@api.route("/profile")
class ProfileAPI(Resource):
    @api.doc("get the oncologist's profile")
    @api.response(200, "Oncologist profile")
    @api.marshal_with(OncologistDto.oncologist_profile, envelope="data")
    @require_logged_in_as(oncologist=True, throughpass=True)
    def get(self, person):
        return get_profile(person.id)


@api.route("/profile/<id>")
class ProfileIdAPI(Resource):
    @api.doc("get the oncologist's profile")
    @api.response(200, "oncologist profile")
    @api.marshal_with(OncologistDto.oncologist_profile, envelope="data")
    def get(self, id):
        return get_profile(id)


@api.route("/list")
class ListAPI(Resource):
    @api.doc("list of oncologists")
    @api.marshal_list_with(PersonDto.person_profile, envelope="data")
    def get(self):
        return get_all_oncologists()
