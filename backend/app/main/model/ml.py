import datetime
import logging
import os
from typing import Dict, List

from psycopg2.extras import execute_values

from app.main.mogonet.main_mogonet import main
from app.main.util.database import UniqueViolation, db_get_cursor
from app.main.util.exceptions.errors import (
    AlreadyExistsError,
    BadInputError,
    NotFoundError,
)

logger = logging.getLogger("mogonet")


class MLModel(object):
    """Representation of a trained MOGONET model."""

    def __init__(
        self,
        id: int,
        name: str,
        time_created: datetime.datetime,
        num_epoch_pretrain: int,
        num_epoch: int,
        lr_e_pretrain: float,
        lr_e: float,
        lr_c: float,
        num_classes: int,
    ):
        self._id = id
        self._name = name
        self._time_created = time_created
        self._num_epoch_pretrain = num_epoch_pretrain
        self._num_epoch = num_epoch
        self._lr_e_pretrain = lr_e_pretrain
        self._lr_e = lr_e
        self._lr_c = lr_c
        self._num_class = num_classes

    @staticmethod
    def new_model(
        name,
        num_epoch_pretrain=500,
        num_epoch=2500,
        lr_e_pretrain=1e-3,
        lr_e=5e-4,
        lr_c=1e-3,
    ) -> "MLModel":
        """Creates a new machine learning model entry in the database.

        Args:
            name (str): The name of the model. Must be either "BRCA" or "ROSMAP".
            num_epoch_pretrain (int, optional): Number of epochs for pretraining. Default is 500.
            num_epoch (int, optional): Number of epochs for training. Default is 2500.
            lr_e_pretrain (float, optional): Learning rate for encoder during pretraining. Default is 1e-3.
            lr_e (float, optional): Learning rate for encoder during training. Default is 5e-4.
            lr_c (float, optional): Learning rate for classifier. Default is 1e-3.

        Returns:
            MLModel: The created MLModel object.

        Raises:
            BadInputError: If the model name is not "BRCA" or "ROSMAP".
            AlreadyExistsError: If a model with the same name already exists.
        """

        name = name.strip().upper()
        if name == "BRCA":
            num_classes = 5
        elif name == "ROSMAP":
            num_classes = 2
        else:
            raise BadInputError("Model name must be either BRCA or ROSMAP")

        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO machine_learning_models (name, num_epoch_pretrain, num_epoch, lr_e_pretrain, lr_e, lr_c, num_classes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        name,
                        num_epoch_pretrain,
                        num_epoch,
                        lr_e_pretrain,
                        lr_e,
                        lr_c,
                        num_classes,
                    ),
                )
                model_id = cur.fetchone()[0]
        except UniqueViolation:
            raise AlreadyExistsError("Model already exists")
        return MLModel.get_by_id(model_id)

    @staticmethod
    def get_by_id(model_id: int) -> "MLModel":
        """Retrieves a machine learning model from the database by its ID.

        Args:
            model_id (int): The ID of the model to retrieve.

        Returns:
            MLModel: The retrieved MLModel object.

        Raises:
            NotFoundError: If no model with the given ID exists.
        """

        with db_get_cursor() as cur:
            cur.execute(
                "SELECT * FROM machine_learning_models WHERE id = %s;", (model_id,)
            )
            result = cur.fetchone()

        try:
            return MLModel(*result)
        except TypeError:
            raise NotFoundError("ML model not found")

    @staticmethod
    def get_all() -> List["MLModel"]:
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM machine_learning_models;")
            result = cur.fetchall()
        return [MLModel(*r) for r in result]

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def time_created(self) -> datetime.datetime:
        return self._time_created

    @property
    def features(self) -> List:
        with db_get_cursor() as cur:
            cur.execute(
                """
                SELECT f.name, m.omics, m.imp
                FROM machine_learning_features m
                    JOIN features f ON m.feat_id = f.id
                WHERE m.model_id = %s;
            """,
                (self._id,),
            )
            result = cur.fetchall()

        return [
            dict(zip(["feat_name", "omics", "imp"], t))
            for t in sorted(result, key=lambda x: x[-1], reverse=True)[:30]
        ]

    @property
    def num_epoch_pretrain(self) -> int:
        return self._num_epoch_pretrain

    @property
    def num_epoch(self) -> int:
        return self._num_epoch

    @property
    def lr_e_pretrain(self) -> float:
        return self._lr_e_pretrain

    @property
    def lr_e(self) -> float:
        return self._lr_e

    @property
    def lr_c(self) -> float:
        return self._lr_c

    @property
    def num_class(self) -> int:
        return self._num_class

    @staticmethod
    def get_feat_dict() -> Dict[str, int]:
        """Retrieves the feature dictionary from the database.

        Returns:
            Dict[str, int]: A dictionary where keys are feature names and values are feature IDs.
        """

        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM features")
            existing = cur.fetchall()
        return {name: id for id, name in existing}

    @staticmethod
    def update_feat_dict(feat_names: List[str]):
        """Updates the feature dictionary in the database with new feature names.

        Args:
            feat_names (List[str]): A list of feature names to be added to the database.

        Returns:
            Dict[str, int]: The updated feature dictionary.
        """

        d = MLModel.get_feat_dict()
        missing = [(n,) for n in feat_names if n not in d]
        with db_get_cursor() as cur:
            execute_values(cur, "INSERT INTO features (name) VALUES %s;", missing)
        return MLModel.get_feat_dict()

    def train(self, threaded=False, thread_dict=None):
        """Trains the machine learning model and updates the performance metrics and features in the database.

        Args:
            threaded (bool, optional): If True, logs the completion of the training thread. Defaults to False.
            thread_dict (dict, optional): A dictionary to update the thread status. Defaults to None.
        """

        performance, features = main(
            os.path.join("app", "main", "mogonet", self.name),
            [1, 2, 3],
            self.num_epoch_pretrain,
            self.num_epoch,
            self.lr_e_pretrain,
            self.lr_e,
            self.lr_c,
            self.num_class,
        )

        # Prepare performance metrics for insertion to database
        metrics = []
        for metric in performance:
            for value in performance[metric][1:]:
                metrics.append((metric, *value, self._id))
        logger.debug(f"Metrics: {metrics}")

        # Prepare features for insertion to database
        feat = [
            list(i.tolist() + (self._id,)) for i in features.to_records(index=False)
        ]
        feat_dict = MLModel.update_feat_dict([f[0] for f in feat])
        for f in feat:
            f[0] = feat_dict[f[0]]
        logger.debug(f"Features: {feat}")

        with db_get_cursor() as cur:
            # Clear all old performance metrics and features for this model
            cur.execute(
                "DELETE FROM machine_learning_performance WHERE model_id = %s;",
                (self._id,),
            )
            cur.execute(
                "DELETE FROM machine_learning_features WHERE model_id = %s;",
                (self._id,),
            )

            execute_values(
                cur,
                """
                INSERT INTO machine_learning_performance (
                    metric_type, epoch, acc, f1_weighted, f1_macro, auc, precision_val, loss, model_id
                ) VALUES %s;
            """,
                metrics,
            )
            execute_values(
                cur,
                "INSERT INTO machine_learning_features (feat_id, omics, imp, model_id) VALUES %s",
                feat,
            )

        if threaded:
            logging.getLogger("threading").info(
                f"Thread training model {self.id} finished."
            )
            thread_dict[self.id] = False

    def get_metrics(self, metric_type, interval):
        """Retrieves the performance metrics for the model from the database.

        Args:
            metric_type (str): The type of metric to retrieve.
            interval (int): The interval at which to retrieve the metrics.

        Returns:
            List[tuple]: A list of tuples containing the performance metrics.

        Raises:
            BadInputError: If metric_type or interval is not provided.
        """

        if not metric_type or not interval:
            raise BadInputError

        with db_get_cursor() as cur:
            cur.execute(
                """
                SELECT epoch, acc, f1_weighted, f1_macro, auc, precision_val, loss
                FROM machine_learning_performance
                WHERE metric_type = %s AND model_id = %s;
            """,
                (metric_type, self.id),
            )
            result = cur.fetchall()

        return [x for x in result if (x[0] % interval == 0)]

    def feedback(self, data):
        """Updates the feedback for the features in the database.

        Args:
            data (list): A list of dictionaries containing feedback and feature names.
        """

        with db_get_cursor() as cur:
            for f in data:
                cur.execute(
                    """
                    UPDATE machine_learning_features
                    SET feedback = %s
                    FROM features
                    WHERE features.id = machine_learning_features.feat_id
                        AND features.name = %s
                        AND machine_learning_features.model_id = %s;
                """,
                    (f["feedback"], f["feature"], self.id),
                )
