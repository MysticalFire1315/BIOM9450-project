from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="authentication related operations")
    user_login = api.model(
        "auth_login",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password "),
        },
    )
    user_register = api.model(
        "auth_register",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password "),
            "username": fields.String(
                required=True, description="The user's public username"
            ),
        },
    )


class UserDto:
    api = Namespace("user", description="user related operations")
    user_link = api.model(
        "user_link",
        {
            "person_id": fields.Integer(
                required=True, description="Id of the person to link current user with"
            ),
        },
    )
    user_profile = api.model(
        "user_profile",
        {
            "email": fields.String(description="The email address"),
            "username": fields.String(description="The user's public username"),
        },
    )


class PersonDto:
    api = Namespace("person", description="person related operations")
    person_profile = api.model(
        "person_profile",
        {
            "firstname": fields.String(description="First name"),
            "lastname": fields.String(description="Last name"),
            "date_of_birth": fields.Date(description="Date of birth"),
            "sex": fields.String(description="Sex")
        },
    )


class PatientDto:
    api = Namespace("patient", description="patient related operations")
    patient_profile = api.model(
        "patient_profile",
        {
            "photo": fields.String(description="Base64 encoded image"),
            "address": fields.String(description="Address (full)"),
            "country": fields.String(description="Country"),
            "emergency_contact_name": fields.String(
                description="Emergency contact name"
            ),
            "emergency_contact_phone": fields.String(
                description="Emergency contact phone number"
            ),
            "person": fields.Nested(PersonDto.person_profile),
        },
    )


class OncologistDto:
    api = Namespace("oncologist", description="oncologist related operations")
    oncologist_profile = api.model(
        "oncologist_profile",
        {
            # Other fields here
            "person": fields.Nested(PersonDto.person_profile),
        },
    )

class ResearcherDto:
    api = Namespace("researcher", description="researcher related operations")
    researcher_profile = api.model(
        "researcher_profile",
        {
            # Other fields here
            "person": fields.Nested(PersonDto.person_profile),
        },
    )
