import datetime
import logging
import threading
from typing import Dict, Tuple

from app.main.model.ml import MLModel
from app.main.util.exceptions.errors import UnavailableError

ESTIMATE = datetime.timedelta(minutes=12)  # CHANGE THIS
MOGONET_THREADS = {}


def train_model(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Trains a new machine learning model.

    Args:
        data (Dict[str, str]): A dictionary containing model training parameters.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing a response message and a status code.
    """

    model = MLModel.new_model(
        data.get("name"),
        data.get("num_epoch_pretrain", 100),
        data.get("num_epoch", 500),
        data.get("lr_e_pretrain", 1e-3),
        data.get("lr_e", 5e-4),
        data.get("lr_c", 1e-3),
    )
    MOGONET_THREADS[model.id] = True

    # Run training in background thread
    thread = threading.Thread(
        target=model.train, args=(True, MOGONET_THREADS), daemon=True
    )
    logging.getLogger("threading").info(f"Thread training model {model.id} started.")
    thread.start()

    return {
        "status": "success",
        "id": model.id,
        "estimated_time": ESTIMATE.total_seconds(),
    }, 202


def get_model(model_id: int):
    """Retrieves a machine learning model by its ID.

    Args:
        model_id (int): The ID of the model to retrieve.

    Returns:
        MLModel: The retrieved MLModel object.

    Raises:
        UnavailableError: If the model is still being trained.
    """

    model_id = int(model_id)
    if model_id in MOGONET_THREADS.keys() and MOGONET_THREADS[model_id]:
        raise UnavailableError("Model still being trained")
    return MLModel.get_by_id(model_id)


def get_models():
    """Retrieves all machine learning models.

    Returns:
        List[MLModel]: A list of all MLModel objects.
    """

    models = MLModel.get_all()
    for m in models:
        m.ready = not (m.id in MOGONET_THREADS.keys() and MOGONET_THREADS[m.id])
    return models


def get_probability(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Calculates the probability of getting cancer based on model features.

    Args:
        data (Dict[str, str]): A dictionary containing model ID and feature expression levels.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing the probability and a status code.
    """

    features = get_model(data["model_id"]).features

    # Probability of getting cancer given by following formula:
    #   sum(expression level * feature importance)/sum(100*feature importance)
    exp_imp = 0
    imp_scale = 0
    for feat in features:
        name = feat["feat_name"]
        imp = feat["imp"]

        exp_imp += max(0, min(data.get(name, 0), 100)) * imp
        imp_scale += 100 * imp

    return {"status": "success", "probability": exp_imp / imp_scale}, 200


def get_metrics(data: Dict[str, str]):
    """Retrieves the performance metrics for a model.

    Args:
        data (Dict[str, str]): A dictionary containing model ID, metric type, and interval.

    Returns:
        List[Dict[str, Union[int, float]]]: A list of dictionaries containing the performance metrics.
    """

    model = get_model(data["model_id"])
    metrics = model.get_metrics(data.get("metric_type"), data.get("interval"))
    keys = ["epoch", "acc", "f1_weighted", "f1_macro", "auc", "precision_val", "loss"]
    return [dict(zip(keys, t)) for t in metrics]


def feedback(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Saves feedback for a model.

    Args:
        data (Dict[str, str]): A dictionary containing model ID and feedback data.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing a response message and a status code.
    """

    model = get_model(data["model_id"])
    model.feedback(data["data"])
    return {"status": "success", "message": "Your feedback has been saved!"}, 201
