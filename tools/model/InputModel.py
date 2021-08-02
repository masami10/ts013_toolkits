from typing import Any


class InputModel:

    def __init__(self):
        self._data = {"inputs": {}, "results": {}}  # input 和result缓存数据

    @property
    def inputs(self):
        return self._data.get("inputs")

    @property
    def results(self):
        return self._data.get("results")

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
