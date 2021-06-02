import json
from loguru import logger
from typing import List
import pandas as pd


class MOMOrder(object):
    def __init__(self, orderNo: str, orderType: str, partNo: str):
        self.wipOrderNo = orderNo  # 订单号
        self.wipOrderType = orderType  # 订单类型
        self.partName = partNo  # 产成品料号

    def as_dict(self):
        return {
            '订单号': self.wipOrderNo,
            '订单类型': self.wipOrderType,
            '产成品': self.partName
        }


class ToolsInfo(object):
    def __init__(self, toolFixedInspectionCode: str = '', toolClassificationCode: str = '', toolMaterialCode: str = '',
                 toolRfid: str = '', toolName: str = '', toolSpecificationType: str = ''):
        self.toolName = toolName
        self.toolClassificationCode = toolClassificationCode
        self.toolFixedInspectionCode = toolFixedInspectionCode
        self.toolMaterialCode = toolMaterialCode
        self.toolRfid = toolRfid
        self.toolSpecificationType = toolSpecificationType

    @property
    def to_dict(self):
        return {
            'toolName': self.toolName,
            'toolClassificationCode': self.toolClassificationCode,
            'toolFixedInspectionCode': self.toolFixedInspectionCode,
            'toolMaterialCode': self.toolMaterialCode,
            'toolRfid': self.toolRfid,
            'toolSpecificationType': self.toolSpecificationType,
        }

    def update(self, tools_info: dict):
        for key, value in tools_info.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Person(object):
    _name = ''
    _number = ''

    def set_name(self, name: str = ''):
        self._name = name

    def set_number(self, number: str = ''):
        self._number = number

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number


class checkValue(object):
    def __init__(self, target: float):
        self.targetValue = target
        self.measure_torque_values: List[float] = []
        self.remeasure_torque_values: List[float] = []
        self._checkResult = 0
        self._recheckResult = 0
        self.checkPerson = Person()
        self.recheckPerson = Person()

    def update_measure(self, val: float, opt: str = 'measure_torque_values'):
        entry: List[float] = getattr(self, opt)
        ll = len(entry)
        if ll < 3:
            entry.append(val)
        entry[2] = val

    def update_measures(self, vals: List[float], opt: str = 'measure_torque_values'):
        entry: List[float] = getattr(self, opt)
        entry = vals

    @property
    def checkValue1(self):
        ll = len(self.measure_torque_values)
        if ll == 0:
            return 0.0
        return self.measure_torque_values[0]

    @property
    def checkValue2(self):
        ll = len(self.measure_torque_values)
        if ll <= 1:
            return 0.0
        return self.measure_torque_values[1]

    @staticmethod
    def validCheckResult(result: bool) -> int:
        if result:
            return 1
        return 0

    def setCheckResult(self, result: bool):
        val = self.validCheckResult(result)
        self._checkResult = val

    def setReCheckResult(self, result: bool):
        val = self.validCheckResult(result)
        self._recheckResult = val

    @property
    def checkResult(self) -> int:
        return self._checkResult

    @property
    def recheckResult(self) -> int:
        return self._recheckResult

    @property
    def checkValue3(self):
        ll = len(self.measure_torque_values)
        if ll <= 2:
            return 0.0
        return self.measure_torque_values[2]

    @property
    def maxCheckValue(self) -> float:
        ll = len(self.measure_torque_values)
        if ll == 0:
            return 0.0
        return max(self.measure_torque_values)

    @property
    def minCheckValue(self) -> float:
        ll = len(self.measure_torque_values)
        if ll == 0:
            return 0.0
        return min(self.measure_torque_values)

    @property
    def maxRecheckValue(self) -> float:
        ll = len(self.remeasure_torque_values)
        if ll == 0:
            return 0.0
        return max(self.remeasure_torque_values)

    @property
    def minReCheckValue(self) -> float:
        ll = len(self.remeasure_torque_values)
        if ll == 0:
            return 0.0
        return min(self.remeasure_torque_values)


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
