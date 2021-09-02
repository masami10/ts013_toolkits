import os
import json
from loguru import logger
from pprint import pformat
from utils.tools import mom_order_2_list
from typing import List, Union
from store.types import MOMOrder, ToolsInfo, checkValue, ToolsTorqueInfo
from transport.constants import now
from sqlite3 import Connection
from store.sql import query_calibration_id_via_identity, insert_ts013_tool_calibration_item

ENV_MOM_WSDL_USER = os.getenv('ENV_MOM_WSDL_USER', 'mtdl001')
ENV_MOM_WSDL_PWD = os.getenv('ENV_MOM_WSDL_PWD', '123456')


def publish_calibration_parameter(rid: int, orders: List[MOMOrder], tool_info: ToolsInfo, check: checkValue) -> dict:
    return {
        "id": rid,
        "toolFixedInspectionCode": tool_info.toolFixedInspectionCode,
        "toolClassificationCode": tool_info.toolClassificationCode,
        "toolMaterialCode": tool_info.toolMaterialCode,
        "toolRfid": tool_info.toolRfid,
        "toolName": tool_info.toolName,
        "toolSpecificationType": tool_info.toolSpecificationType,
        "checkValue": check.targetValue,
        "maxCheckValue": check.maxCheckValue,
        "minCheckValue": check.minCheckValue,
        "maxRecheckValue": check.maxRecheckValue,
        "minRecheckValue": check.minCheckValue,
        "checkTime": now(),
        "checkValue1": check.checkValue1,
        "checkValue2": check.checkValue2,
        "checkValue3": check.checkValue3,
        "checkEmployeeNo": check.checkPerson.number,
        "checkEmployeeName": check.checkPerson.name,
        "checkResult": check.checkResult,
        "recheckTime": now(),
        "recheckValue": 0.0,
        "recheckEmployeeNo": check.recheckPerson.number,
        "recheckEmployeeName": check.recheckPerson.name,
        "recheckResult": check.recheckResult,
        "momOrders": mom_order_2_list(orders)
    }


def publish_calibration_payload(rid: int, orders: List[MOMOrder], tool_info: ToolsInfo, check: checkValue) -> dict:
    param = publish_calibration_parameter(rid, orders, tool_info, check)
    return {
        "MethodName": "TorqueCheckInfo",
        "Parameter": param
    }


def publish_calibration_value_2_mes_wsdl(conn: Connection, tool_sn: str, orders: List[MOMOrder],
                                         tool_info: ToolsTorqueInfo,
                                         check: checkValue, raw=False) -> Union[dict, str]:
    ss = [o.wipOrderNo for o in orders]
    str_orders = ",".join(ss)
    identity = f"{tool_sn}@{str_orders}"
    c_id = query_calibration_id_via_identity(conn, identity)
    if not c_id:
        rid = insert_ts013_tool_calibration_item(conn, identity)
        conn.commit()
    else:
        rid = c_id
    payload = publish_calibration_payload(rid, orders, tool_info, check)
    return payload
