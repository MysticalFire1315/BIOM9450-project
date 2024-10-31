from typing import Dict, Tuple

from app.main.service.user_service import link_user
from app.main.util.decorator import require_user_logged_in
from app.main.util.dto import UserDto
from flask import request
from flask_restx import Resource

api = UserDto.api

@api.route("/link")
class UserLink(Resource):
    @api.doc("link a user to an existing person profile")
    @api.expect(UserDto.user_link, validate=True)
    @api.response(200, "Successfully linked")
    @require_user_logged_in(throughpass=True)
    def post(self, user) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return link_user(user, post_data)



# @UserDto.api.route("/")
# class UserList(Resource):
#     @UserDto.api.doc("list_of_registered_users")
#     @admin_token_required
#     @UserDto.api.marshal_list_with(UserDto.user, envelope="data")
#     def get(self):
#         """List all registered users"""
#         return get_all_users()

#     @UserDto.api.expect(UserDto.user, validate=True)
#     @UserDto.api.response(201, "User successfully created.")
#     @UserDto.api.doc("create a new user")
#     def post(self) -> Tuple[Dict[str, str], int]:
#         """Creates a new User"""
#         data = request.json
#         return save_new_user(data=data)


# @UserDto.api.route("/<public_id>")
# @UserDto.api.param("public_id", "The User identifier")
# @UserDto.api.response(404, "User not found.")
# class User(Resource):
#     @UserDto.api.doc("get a user")
#     @UserDto.api.marshal_with(UserDto.user)
#     def get(self, public_id):
#         """get a user given its identifier"""
#         user = get_a_user(public_id)
#         if not user:
#             api.abort(404)
#         else:
#             return user
