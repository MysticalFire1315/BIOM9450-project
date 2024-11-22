from app.main.model.ml import MLModel

def get_model(id: int):
    return MLModel.get_by_id(id)