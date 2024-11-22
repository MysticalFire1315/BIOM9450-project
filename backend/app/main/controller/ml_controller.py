from app.main.service.ml_service import get_model
from app.main.util.dto import MachineLearningDto
from app.main.util.decorators import require_logged_in_as
from flask_restx import Resource

api = MachineLearningDto.api

@api.route("/model/<id>")
class ModelAPI(Resource):
    @api.doc("get the model")
    @api.response(200, "Model")
    @api.marshal_with(MachineLearningDto.ml_model, envelope="data")
    @require_logged_in_as(researcher=True)
    def get(self, id):
        return get_model(id)
