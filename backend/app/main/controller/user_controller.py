from typing import Dict, Tuple

from app.main.service.user_service import check_link, link_user, get_user, user_history
from app.main.util.decorator import require_user_logged_in
from app.main.util.dto import UserDto
from flask import request
from flask_restx import Resource

api = UserDto.api

@api.route("/link")
class LinkAPI(Resource):
    @api.doc("check if user is linked")
    @api.response(200, "True or false depending whether the logged in user is linked")
    @require_user_logged_in(throughpass=True)
    def get(self, user) -> Tuple[Dict[str, str], int]:
        return check_link(user)

    @api.doc("link a user to an existing person profile")
    @api.expect(UserDto.user_link, validate=True)
    @api.response(200, "Successfully linked")
    @require_user_logged_in(throughpass=True)
    def post(self, user) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return link_user(user, post_data)

@api.route("/profile")
class ProfileAPI(Resource):
    @api.doc("get the user's profile")
    @api.response(200, "User profile")
    @api.marshal_with(UserDto.user_profile, envelope="data")
    @require_user_logged_in(throughpass=True)
    def get(self, user):
        return get_user(user)

@api.route("/history/<n>")
class HistoryAPI(Resource):
    @api.doc("get the last `n` requests made by the current user")
    @api.marshal_list_with(UserDto.user_history)
    @require_user_logged_in(throughpass=True)
    def get(self, user, n):
        return user_history(user, int(n))

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
