import datetime
from typing import List

from app.main.util.database import db_get_cursor
from app.main.util.exceptions.errors import NotFoundError, BadInputError

class MLModel(object):
    def __init__(
        self,
        id: int,
        name: str,
        time_created: datetime.datetime
    ):
        self._id = id
        self._name = name
        self._time_created = time_created

    @staticmethod
    def get_by_id(id: int) -> "ML":
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
        return [{
            "feat_name": feat_name,
            "omics": omics,
            "imp": imp,
        } for feat_name, omics, imp in result]