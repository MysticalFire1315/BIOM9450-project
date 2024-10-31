from functools import partial, wraps

from flask import request

from app.main.service.auth_service import get_logged_in_person, get_logged_in_user
from typing import Callable

def require_user_logged_in(
    func: Callable = None, /, *, throughpass=False
) -> Callable:
    """Require a user to be logged in to access the route.

    Args:
        func (Callable, optional): Controller function being wrapped. Defaults to None.
        throughpass (bool, optional): If set to True, pass `User` object representing logged in user
            to the wrapped function as keyword argument "user". Defaults to False.

    Returns:
        Callable: The specified function if the user is logged in. Otherwise returns an error message
        and status code.
    """

    if not func:
        return partial(
            require_user_logged_in,
            throughpass=throughpass
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = get_logged_in_user(request.headers.get("Authorization"))
        if type(resp) is tuple:
            return resp
        # otherwise resp is user

        if throughpass:
            kwargs['user'] = resp
        return func(*args, **kwargs)

    return wrapper


def require_logged_in_as(
    func: Callable = None, /, *, patient=False, oncologist=False, researcher=False, throughpass=False
) -> Callable:
    """Require a user to be logged in to access the route.
    Optionally, the user can be required to be a patient, oncologist, or researcher.

    Args:
        func (Callable, optional): Controller function being wrapped. Defaults to None.
        patient (bool, optional): If set to True, allow access to any user with the role `Patient`.
            Defaults to False.
        oncologist (bool, optional): If set to True, allow access to any user with the role `Oncologist`.
            Defaults to False.
        researcher (bool, optional): If set to True, allow access to any user with the role `Researcher`.
            Defaults to False.
        throughpass (bool, optional): If set to True, pass `Person` object representing logged in person
            to the wrapped function as keyword argument "person". Defaults to False.

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
            throughpass=throughpass
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

        if throughpass:
            kwargs['person'] = resp
        return func(*args, **kwargs)

    return wrapper
