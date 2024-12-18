from flask import Blueprint
from flask_restx import Api

from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.ml_controller import api as ml_ns
from app.main.controller.mutations_controller import api as mutations_ns
from app.main.controller.oncologist_controller import api as oncologist_ns
from app.main.controller.patient_controller import api as patient_ns
from app.main.controller.person_controller import api as person_ns
from app.main.controller.researcher_controller import api as researcher_ns
from app.main.controller.user_controller import api as user_ns
from app.main.util.exceptions.handlers import register_handlers

blueprint = Blueprint("api", __name__)
authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    blueprint,
    title="FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT",
    version="1.0",
    description="a boilerplate for flask restplus (restx) web service",
    authorizations=authorizations,
    security="apikey",
)

# Register namespaces
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(user_ns, path="/user")
api.add_namespace(person_ns, path="/person")
api.add_namespace(patient_ns, path="/patient")
api.add_namespace(oncologist_ns, path="/oncologist")
api.add_namespace(researcher_ns, path="/researcher")
api.add_namespace(ml_ns, path="/ml")
api.add_namespace(mutations_ns, path="/mutations")

register_handlers(api)
