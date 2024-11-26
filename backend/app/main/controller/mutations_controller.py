from flask_restx import Resource

from app.main.service.mutations_service import get_all_mutations, get_mutation
from app.main.util.decorator import require_logged_in_as
from app.main.util.dto import MutationDto

api = MutationDto.api


@api.route("/list")
class ListAPI(Resource):
    @api.doc("list all mutations")
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self):
        return get_all_mutations()


@api.route("/<name>")
class ProfileAPI(Resource):
    @api.doc("get the mutation")
    @api.marshal_with(MutationDto.mutation_profile)
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self, name):
        return get_mutation(name)
