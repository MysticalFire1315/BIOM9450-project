import datetime
import logging
import os
from typing import List
from psycopg2.extras import execute_values

from app.main.util.database import db_get_cursor, UniqueViolation
from app.main.util.exceptions.errors import NotFoundError, AlreadyExistsError, BadInputError
from app.main.mogonet.main_mogonet import main

logger = logging.getLogger("mogonet")

class MLModel(object):
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
        num_classes:int
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
    def new_model(name, num_epoch_pretrain=500, num_epoch=2500, lr_e_pretrain=1e-3, lr_e=5e-4, lr_c=1e-3) -> "MLModel":
        name = name.strip().upper()
        if name == 'BRCA':
            num_classes = 5
        elif name == 'ROSMAP':
            num_classes = 2
        else:
            raise BadInputError('Model name must be either BRCA or ROSMAP')

        try:
            with db_get_cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO machine_learning_models (name, num_epoch_pretrain, num_epoch, lr_e_pretrain, lr_e, lr_c, num_classes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (name, num_epoch_pretrain, num_epoch, lr_e_pretrain, lr_e, lr_c, num_classes),
                )
                model_id = cur.fetchone()[0]
        except UniqueViolation:
            raise AlreadyExistsError('Model already exists')
        return MLModel.get_by_id(model_id)

    @staticmethod
    def get_by_id(id: int) -> "MLModel":
        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM machine_learning_models WHERE id = %s;", (id,))
            result = cur.fetchone()

        try:
            return MLModel(*result)
        except TypeError:
            raise NotFoundError('ML model not found')

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
            cur.execute("SELECT feat_name, omics, imp FROM machine_learning_features WHERE model_id = %s;", (self._id,))
            result = cur.fetchall()
        return [dict(zip(["feat_name", "omics", "imp"], t)) for t in result]

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

    def train(self, threaded=False, thread_dict=None):
        performance, features = main(os.path.join("app", "main", "mogonet", self.name), [1, 2, 3], self.num_epoch_pretrain, self.num_epoch, self.lr_e_pretrain, self.lr_e, self.lr_c, self.num_class)

        # Prepare performance metrics for insertion to datebase
        metrics = []
        for metric in performance:
            for value in performance[metric][1:]:
                metrics.append((metric, *value, self._id))
        logger.debug(f"Metrics: {metrics}")

        # Prepare features for insertion to database
        feat = [i.tolist() + (self._id,) for i in features.to_records(index=False)]
        logger.debug(f"Features: {feat}")

        with db_get_cursor() as cur:
            # Clear all old performance metrics and features for this model
            cur.execute("DELETE FROM machine_learning_performance WHERE model_id = %s;", (self._id,))
            cur.execute("DELETE FROM machine_learning_features WHERE model_id = %s;", (self._id,))

            execute_values(cur, """
                INSERT INTO machine_learning_performance (
                    metric_type, epoch, acc, f1_weighted, f1_macro, auc, precision_val, loss, model_id
                ) VALUES %s;
            """, metrics)
            execute_values(cur, "INSERT INTO machine_learning_features (feat_name, omics, imp, model_id) VALUES %s", feat)

        if threaded:
            logging.getLogger("threading").info(f"Thread training model {self.id} finished.")
            thread_dict[self.id] = False

    def get_metrics(self, metric_type, interval):
        if not metric_type or not interval:
            raise BadInputError

        with db_get_cursor() as cur:
            cur.execute("""
                SELECT epoch, acc, f1_weighted, f1_macro, auc, precision_val, loss
                FROM machine_learning_performance
                WHERE metric_type = %s and model_id = %s;
            """, (metric_type, self.id))
            result = cur.fetchall()

        return [x for x in result if (x[0] % interval == 0)]

    def feedback(self, data):
        with db_get_cursor() as cur:
            for f in data:
                cur.execute("""
                    UPDATE machine_learning_features
                    SET feedback = %s
                    WHERE feat_name = %s and model_id = %s;
                """, (f["feedback"], f["feature"], self.id))
