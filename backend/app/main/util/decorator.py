from functools import partial, wraps

from flask import request

from app.main.service.auth_helper import get_logged_in_person
from typing import Callable


def require_logged_in(
    func: Callable = None, /, *, patient=False, oncologist=False, researcher=False
) -> Callable:
    """Require a user to be logged in to access the route.
    Optionally, the user can be required to be a patient, oncologist, or researcher.

    Args:
        func (Callable, optional): Controller function should always take `User` as first argument.
            Defaults to None.
        patient (bool, optional): If set to True, allow access to any user with the role `Patient`.
            Defaults to False.
        oncologist (bool, optional): If set to True, allow access to any user with the role `Oncologist`.
            Defaults to False.
        researcher (bool, optional): If set to True, allow access to any user with the role `Researcher`.
            Defaults to False.

    Returns:
        Callable: The specified function if the user is logged in with the correct role. Otherwise
        returns an error message and status code.
    """

    if not func:
        return partial(
            require_logged_in,
            patient=patient,
            oncologist=oncologist,
            researcher=researcher,
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = get_logged_in_person(request.headers.get("Authorization"))
        if type(resp) is tuple:
            return resp
        # otherwise resp is person

        if not (
            (resp.role == "patient" and patient)
            or (resp.role == "oncologist" and oncologist)
            or (resp.role == "researcher" and researcher)
        ):
            return {"status": "fail", "message": "Unauthorized"}, 403
        return func(resp, *args, **kwargs)

    return wrapper
