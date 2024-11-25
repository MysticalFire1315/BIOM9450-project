from app.main.service.mutations_service import get_all_mutations, get_mutation
from app.main.util.dto import MutationDto
from app.main.util.decorator import require_logged_in_as
from flask_restx import Resource

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
    @api.response(200, "Mutation")
    @api.expect(MutationDto.mutation_profile)
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self, name):
        return get_mutation(name)