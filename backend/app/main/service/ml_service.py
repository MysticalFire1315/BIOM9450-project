from app.main.model.ml import MLModel
from typing import Dict, Tuple

def get_model(id: int):
    return MLModel.get_by_id(id)

def get_probability(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    features = MLModel.get_by_id(data["model_id"]).features

    exp_imp = 0
    imp_scale = 0

    for feat in features:
        name = feat["feat_name"]
        imp = feat["imp"]

        exp_imp += max(0, min(data.get(name, 0), 100)) * imp
        imp_scale += 100 * imp

    return {"status": "success", "probability": exp_imp / imp_scale}, 200