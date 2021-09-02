from pandas import DataFrame

from py_singleton import singleton


@singleton
class CheckResultModel:
    _results: DataFrame

    _tail_count = 3

    def __init__(self):
        self._results = DataFrame({
            'count': [],
            'date': [],
            'time': [],
            'torque': [],
            'angle': [],
            'result': []
        })

    @property
    def results(self) -> DataFrame:
        return self._results

    def clear_results(self):
        self._results = DataFrame({
            'count': [],
            'date': [],
            'time': [],
            'torque': [],
            'angle': [],
            'result': []
        })

    def append_result(self, count, date, time, torque, angle, result):
        self._results = self._results.append(DataFrame({
            'count': [count],
            'date': [date],
            'time': [time],
            'torque': [torque],
            'angle': [angle],
            'result': [result]
        }), ignore_index=True).tail(self._tail_count)

    def results_all_ok(self, max_torque, min_torque):
        torques = list(self._results['torque'])
        return all(map(lambda t: not self.is_result_nok(t, max_torque, min_torque), torques)) if len(torques) > 0 else False

    def results_last_ok(self, max_torque, min_torque):
        torques = list(self._results['torque'])
        return not self.is_result_nok(torques[-1], max_torque, min_torque) if len(torques) > 0 else False

    @staticmethod
    def is_result_nok(torque, max_torque, min_torque) -> bool:
        if max_torque is None and min_torque is None:
            return False
        if torque is None:
            return True
        if min_torque is not None and float(min_torque) > float(torque):
            return True
        if max_torque is not None and float(max_torque) < float(torque):
            return True
        return False


check_result_model_instance = CheckResultModel()
