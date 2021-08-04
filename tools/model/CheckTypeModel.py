from py_singleton import singleton


@singleton
class CheckTypeModel:

    def __init__(self):
        self._is_first_check = None

    @property
    def is_first_check(self) -> bool:
        return self._is_first_check

    def set_is_first_check(self, val: bool):
        self._is_first_check = bool(val)

    @property
    def did_set(self) -> bool:
        return self._is_first_check is not None


check_type_model_instance = CheckTypeModel()
