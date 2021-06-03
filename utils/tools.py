import json
from typing import List


def serialize_obj_2_json(orders: List[object]) -> str:
    data = [ob.__dict__ for ob in orders]
    j_data = json.dumps(data)
    return j_data
