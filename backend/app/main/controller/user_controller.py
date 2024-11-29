from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from app.main.service.user_service import check_link, get_user, link_user, user_history
from app.main.util.decorator import require_user_logged_in
from app.main.util.dto import UserDto

api = UserDto.api


@api.route("/link")
class LinkAPI(Resource):
    @api.doc("check if user is linked")
    @require_user_logged_in(throughpass=True)
    def get(self, user) -> Tuple[Dict[str, str], int]:
        return check_link(user)

    @api.doc("link a user to an existing person profile")
    @api.expect(UserDto.user_link, validate=True)
    @api.response(201, "Successfully linked")
    @require_user_logged_in(throughpass=True)
    def post(self, user) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return link_user(user, post_data)


@api.route("/profile")
class ProfileAPI(Resource):
    @api.doc("get the user's profile")
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
