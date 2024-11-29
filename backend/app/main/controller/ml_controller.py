from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from app.main.service.ml_service import (
    feedback,
    get_metrics,
    get_model,
    get_models,
    get_probability,
    train_model,
)
from app.main.util.decorator import require_logged_in_as
from app.main.util.dto import MachineLearningDto

api = MachineLearningDto.api


@api.route("/list")
class ListAPI(Resource):
    @api.doc("list all models")
    @api.marshal_list_with(MachineLearningDto.ml_model, envelope="data", skip_none=True)
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self):
        return get_models()


@api.route("/model/<id>")
class ModelAPI(Resource):
    @api.doc("get the model")
    @api.marshal_with(MachineLearningDto.ml_model, envelope="data", skip_none=True)
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self, id):
        return get_model(id)


@api.route("/probability")
class ProbabilityAPI(Resource):
    @api.doc("determine probability from model")
    @api.expect(MachineLearningDto.ml_expressions)
    @require_logged_in_as(oncologist=True, researcher=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return get_probability(post_data)


@api.route("/train")
class TrainAPI(Resource):
    @api.doc("train a model")
    @api.response(202, "Model training started")
    @api.expect(MachineLearningDto.ml_train)
    @require_logged_in_as(oncologist=True, researcher=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return train_model(post_data)


@api.route("/metrics")
class MetricsAPI(Resource):
    @api.doc("get metrics about a model")
    @api.expect(MachineLearningDto.ml_metrics_input)
    @api.marshal_list_with(MachineLearningDto.ml_metrics_output)
    @require_logged_in_as(oncologist=True, researcher=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return get_metrics(post_data)


@api.route("/feedback")
class FeedbackAPI(Resource):
    @api.doc("provide feedback")
    @api.response(201, "Feedback saved successfully")
    @api.expect(MachineLearningDto.ml_feedback)
    @require_logged_in_as(oncologist=True, researcher=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return feedback(post_data)
