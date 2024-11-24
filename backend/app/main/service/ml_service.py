from app.main.model.ml import MLModel
from app.main.util.exceptions.errors import UnavailableError, NotFoundError
from typing import Dict, Tuple
import threading
import datetime
import logging

ESTIMATE = datetime.timedelta(minutes=12) # CHANGE THIS
MOGONET_THREADS = {}

def train_model(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    model = MLModel.new_model(
        data.get('name'),
        data.get('num_epoch_pretrain', 100),
        data.get('num_epoch', 500),
        data.get('lr_e_pretrain', 1e-3),
        data.get('lr_e', 5e-4),
        data.get('lr_c', 1e-3)
    )
    MOGONET_THREADS[model.id] = True

    thread = threading.Thread(target=model.train, args=(True, MOGONET_THREADS), daemon=True)
    logging.getLogger("threading").info(f"Thread training model {model.id} started.")
    thread.start()

    return {"status": "success", "id": model.id, "estimated_time": ESTIMATE.total_seconds()}, 202

def get_model(id: int):
    id = int(id)
    if id in MOGONET_THREADS.keys() and MOGONET_THREADS[id]:
        raise UnavailableError("Model still being trained")
    return MLModel.get_by_id(id)

def get_probability(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    features = get_model(data["model_id"]).features

    exp_imp = 0
    imp_scale = 0

    for feat in features:
        name = feat["feat_name"]
        imp = feat["imp"]

        exp_imp += max(0, min(data.get(name, 0), 100)) * imp
        imp_scale += 100 * imp

    return {"status": "success", "probability": exp_imp / imp_scale}, 200
