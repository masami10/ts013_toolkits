import json
from typing import List
from qasync import QEventLoop
from store.types import MOMOrder


def mom_order_2_list(orders: List[MOMOrder]) -> List[dict]:
    return [ob.dict() for ob in orders]


def serialize_obj_2_json(orders: List[MOMOrder]) -> str:
    data = mom_order_2_list(orders)
    j_data = json.dumps(data)
    return j_data


def run_and_get_result(coro):
    loop = QEventLoop(already_running=False)
    result = loop.run_until_complete(coro)
    return result
