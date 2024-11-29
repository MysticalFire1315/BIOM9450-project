"""Data Transfer Objects (DTOs) for the Swagger API."""

from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="authentication related operations")
    user_login = api.model(
        "auth_login",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )
    user_register = api.model(
        "auth_register",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
            "username": fields.String(required=True),
        },
    )


class UserDto:
    api = Namespace("user", description="user related operations")
    user_link = api.model(
        "user_link",
        {
            "person_id": fields.Integer(required=True),
        },
    )
    user_profile = api.model(
        "user_profile",
        {
            "email": fields.String(),
            "username": fields.String(),
            "role": fields.String(),
        },
    )
    user_history = api.model(
        "user_history",
        {
            "time_accessed": fields.DateTime(),
            "method": fields.String(),
            "path": fields.String(),
            "response": fields.Integer(),
        },
    )


class PersonDto:
    api = Namespace("person", description="person related operations")
    person_profile = api.model(
        "person_profile",
        {
            "id": fields.Integer(),
            "firstname": fields.String(),
            "lastname": fields.String(),
            "date_of_birth": fields.Date(),
            "sex": fields.String(),
        },
    )


class PatientDto:
    api = Namespace("patient", description="patient related operations")
    patient_profile = api.model(
        "patient_profile",
        {
            "photo": fields.String(),
            "address": fields.String(),
            "country": fields.String(),
            "emergency_contact_name": fields.String(),
            "emergency_contact_phone": fields.String(),
            "person": fields.Nested(PersonDto.person_profile),
        },
    )


class OncologistDto:
    api = Namespace("oncologist", description="oncologist related operations")
    oncologist_profile = api.model(
        "oncologist_profile",
        {
            "specialization": fields.String(),
            "phone": fields.String(),
            "email": fields.String(),
            "affiliations": fields.List(fields.String()),
            "person": fields.Nested(PersonDto.person_profile),
        },
    )


class ResearcherDto:
    api = Namespace("researcher", description="researcher related operations")
    researcher_position = api.model(
        "researcher_position",
        {
            "title": fields.String(),
            "organization": fields.String(),
            "start_date": fields.Date(),
            "end_date": fields.Date(),
        },
    )
    researcher_profile = api.model(
        "researcher_profile",
        {
            "title": fields.String(),
            "phone": fields.String(),
            "email": fields.String(),
            "area_of_research": fields.String(),
            "positions": fields.List(fields.Nested(researcher_position)),
            "person": fields.Nested(PersonDto.person_profile),
        },
    )


class MachineLearningDto:
    api = Namespace(
        "machine_learning", description="machine learning related operations"
    )
    ml_features = api.model(
        "ml_features",
        {
            "feat_name": fields.String(),
            "omics": fields.Integer(),
            "imp": fields.Float(),
        },
    )
    ml_model = api.model(
        "ml_model",
        {
            "name": fields.String(),
            "time_created": fields.DateTime(),
            "features": fields.List(fields.Nested(ml_features)),
            "num_epoch_pretrain": fields.Integer(),
            "num_epoch": fields.Integer(),
            "lr_e_pretrain": fields.Float(),
            "lr_e": fields.Float(),
            "lr_c": fields.Float(),
            "ready": fields.Boolean(),
        },
    )
    ml_expressions = api.model(
        "ml_expressions",
        {
            "model_id": fields.Integer(),
            "*": fields.Wildcard(fields.Float()),
        },
    )
    ml_train = api.model(
        "ml_train",
        {
            "name": fields.String(required=True),
            "num_epoch_pretrain": fields.Integer(),
            "num_epoch": fields.Integer(),
            "lr_e_pretrain": fields.Float(),
            "lr_e": fields.Float(),
            "lr_c": fields.Float(),
        },
    )
    ml_metrics_input = api.model(
        "ml_metrics_input",
        {
            "model_id": fields.Integer(),
            "metric_type": fields.String(),
            "interval": fields.Integer(),
        },
    )
    ml_metrics_output = api.model(
        "ml_metrics_output",
        {
            "epoch": fields.Integer(),
            "acc": fields.Float(),
            "f1_weighted": fields.Float(),
            "f1_macro": fields.Float(),
            "auc": fields.Float(),
            "precision_val": fields.Float(),
            "loss": fields.Float(),
        },
    )
    ml_feature_feedback = api.model(
        "ml_feature_feedback",
        {
            "feature": fields.String(),
            "feedback": fields.String(),
        },
    )
    ml_feedback = api.model(
        "ml_feedback",
        {
            "model_id": fields.Integer(),
            "data": fields.List(fields.Nested(ml_feature_feedback)),
        },
    )


class MutationDto:
    api = Namespace("mutation", description="mutation related operations")
    mutation_cosmic_data = api.model(
        "mutation_cosmic_data",
        {
            "mutation_id": fields.String(),
            "gene_name": fields.String(),
            "primary_site": fields.String(),
        },
    )
    mutation_profile = api.model(
        "mutation_profile",
        {
            "COSMIC_data": fields.List(fields.Nested(mutation_cosmic_data)),
            "patients": fields.List(fields.Integer()),
        },
    )
