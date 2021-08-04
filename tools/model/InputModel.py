from typing import Any, Dict

from py_singleton import singleton

@singleton
class InputModel:

    def __init__(self):
        self._data = {"inputs": {}}  # input缓存数据

    @property
    def inputs(self) -> Dict:
        return self._data.get("inputs")

    def update_inputs_data(self, key: str, val: Any):
        entry = self._data.get("inputs")
        entry.update({key: val})

    def update_results_data(self, key: str, val: Any):
        entry = self._data.get("results")
        entry.update({key: val})

    def get_input(self, *args):
        return self._data.get("inputs", {}).get(*args)

    def get_results(self, *args):
        return self._data.get("results", {}).get(*args)


input_model_instance = InputModel()
