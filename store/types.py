import json
from loguru import logger
from typing import List


class MOMOrder(object):
    def __init__(self, orderNo: str, orderType: str, partNo: str):
        self.wipOrderNo = orderNo
        self.wipOrderType = orderType
        self.partName = partNo


class ToolsInfo(object):
    def __init__(self, toolFixedInspectionCode: str, toolClassificationCode: str, toolMaterialCode: str,
                 toolRfid: str, toolName: str, toolSpecificationType: str):
        self.toolName = toolName
        self.toolClassificationCode = toolClassificationCode
        self.toolFixedInspectionCode = toolFixedInspectionCode
        self.toolMaterialCode = toolMaterialCode
        self.toolRfid = toolRfid
        self.toolSpecificationType = toolSpecificationType


class checkValue(object):
    def __init__(self, target: float):
        self.checkValue = target
        self.measure_values: List[float] = []
        self.remeasure_values: List[float] = []

    def update_measure(self, val: float, opt: str = 'measure_values'):
        entry: List[float] = getattr(self, opt)
        ll = len(entry)
        if ll < 3:
            entry.append(val)
        entry[2] = val

    def update_measures(self, vals: List[float], opt: str = 'measure_values'):
        entry: List[float] = getattr(self, opt)
        entry = vals

    @property
    def checkValue1(self):
        ll = len(self.measure_values)
        if ll == 0:
            return 0.0
        return self.measure_values[0]

    @property
    def checkValue2(self):
        ll = len(self.measure_values)
        if ll <= 1:
            return 0.0
        return self.measure_values[1]

    @property
    def checkResult(self) -> int:
        return 1

    @property
    def recheckResult(self) -> int:
        return 1

    @property
    def checkValue3(self):
        ll = len(self.measure_values)
        if ll <= 2:
            return 0.0
        return self.measure_values[2]

    @property
    def maxCheckValue(self) -> float:
        ll = len(self.measure_values)
        if ll == 0:
            return 0.0
        return max(self.measure_values)

    @property
    def minCheckValue(self) -> float:
        ll = len(self.measure_values)
        if ll == 0:
            return 0.0
        return min(self.measure_values)

    @property
    def maxRecheckValue(self) -> float:
        ll = len(self.remeasure_values)
        if ll == 0:
            return 0.0
        return max(self.remeasure_values)

    @property
    def minReCheckValue(self) -> float:
        ll = len(self.remeasure_values)
        if ll == 0:
            return 0.0
        return min(self.remeasure_values)


class checkInfoParams(object):
    def __init__(self, rid: int, tools_info: ToolsInfo):
        self.id = rid
        self.tools_info = tools_info

    def serialize_json(self):
        ret: dict = self.__dict__
        ret.update(self.tools_info.__dict__)
        try:
            ret.pop('tools_info')
        except Exception as e:
            logger.error(f'serialize_json Error: {e}')
        return json.dumps(ret)
