import json
from typing import List
from qasync import QEventLoop


def serialize_obj_2_json(orders: List[object]) -> str:
    data = [ob.__dict__ for ob in orders]
    j_data = json.dumps(data)
    return j_data


def run_and_get_result(coro):
    loop = QEventLoop(already_running=False)
    result = loop.run_until_complete(coro)
    return result
