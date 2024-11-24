from app.main.service.ml_service import get_model, get_probability, train_model, get_metrics, feedback
from app.main.util.dto import MachineLearningDto
from app.main.util.decorator import require_logged_in_as
from flask_restx import Resource
from flask import request
from typing import Tuple, Dict

api = MachineLearningDto.api

@api.route("/model/<id>")
class ModelAPI(Resource):
    @api.doc("get the model")
    @api.response(200, "Model")
    @api.marshal_with(MachineLearningDto.ml_model, envelope="data")
    @require_logged_in_as(oncologist=True, researcher=True)
    def get(self, id):
        return get_model(id)

@api.route("/probability")
class ProbabilityAPI(Resource):
    @api.doc("determine probability from model")
    @api.response(200, "Probability")
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
    @api.expect(MachineLearningDto.ml_feedback)
    @require_logged_in_as(oncologist=True, researcher=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return feedback(post_data)
