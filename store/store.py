from typing import Any
from py_singleton import singleton


@singleton
class StorageData(object):
    def __init__(self):
        self._data = {}

    def update_data(self, key: str, value: Any):
        self._data.update({key, value})

    def get_data(self, key: str):
        return self._data.get(key, None)

    def __str__(self):
        return 'Global Storage'
