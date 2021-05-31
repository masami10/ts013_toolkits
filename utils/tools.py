import json
from typing import List


def serialize_obj_2_json(orders: List[object]) -> str:
    return json.dumps([ob.__dict__ for ob in orders])

