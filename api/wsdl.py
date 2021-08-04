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

'''
{
    "MethodName":" TorqueCheckInfo",
"Parameter":'{
        "id":100011,
        "toolFixedInspectionCode":"105004014101",
        "toolClassificationCode":"10102016002",
        "toolMaterialCode":"000000001800000181",
        "toolRfid":"315110040000000000000224",
        "toolName":"可调式扭力扳手",
        "toolSpecificationType":"扭矩范围(4-20)N.m",
        "checkValue":55.0,
        "maxCheckValue":56.37,
        "minCheckValue":53.63,
        "maxRecheckValue":57.75,
        "minRecheckValue":52.25,
        "checkTime":"2020-04-2416:27:30",
        "checkValue1":55.0,
        "checkValue2":55.1,
        "checkValue3":55.2,
        "checkEmployeeNo":"65595",
        "checkEmployeeName":"朱亚征",
        "checkResult":1,
        "recheckTime":"2020-04-2416:27:42",
        "recheckValue":55.0,
        "recheckEmployeeNo":"65595",
        "recheckEmployeeName":"朱亚征",
        "recheckResult":1,
        "momOrders":[
            {"wipOrderNo":"001103030335","wipOrderType":"101.0","partName":"混合空气箱安装M4"}
        ]
}'} 


<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:flex="http://www.apriso.com/DELMIAApriso" xmlns:flex1="http://schemas.datacontract.org/2004/07/FlexNet.WebServices">
 <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
 <a:To s:mustUnderstand = "1" xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">
http://172.31.120.56/Apriso/WebServices/Public/MOM_PeripheralSystem_InspectionInfo.svc
 </a:To>
 <wsa:Action>http://www.apriso.com/DELMIAApriso/MOM_PeripheralSystem_InspectionInfo/Invoke</wsa:Action> 
 </soap:Header>

   <soap:Body>
      <flex:Invoke>
         <!--Optional:-->
         <flex:inputs>
            <!--Optional:-->
            <flex1:Input_attr1>?</flex1:Input_attr1>
            <!--Optional:-->
            <flex1:Input_attr2>?</flex1:Input_attr2>
            <!--Optional:-->
            <flex1:Input_attr3>?</flex1:Input_attr3>
            <!--Optional:-->
            <flex1:Input_instId>?</flex1:Input_instId>
            <!--Optional:-->
            <flex1:Input_requestTime>?</flex1:Input_requestTime>
            <!--Optional:-->
<flex1:Parameter>{"MethodName":" ","Parameter":’{id:10001,"toolFixedInspectionCode":"105004014101","toolClassificationCode":"10102016002","toolMaterialCode":"000000001800000181","toolRfid":"315110040000000000000224","toolName":"可调式扭力扳手","toolSpecificationType":"扭矩范围(4-20)N.m","checkValue":55.0,"maxCheckValue":56.37,"minCheckValue":53.63,"maxRecheckValue":57.75,"minRecheckValue":52.25,"checkTime":"2020-04-2416:27:30","checkValue1":55.0,"checkValue2":55.1,"checkValue3":55.2,"checkEmployeeNo":"65595","checkEmployeeName":"朱亚征","checkResult":1,"recheckTime":"2020-04-2416:27:42","recheckValue":55.0,"recheckEmployeeNo":"65595","recheckEmployeeName":"朱亚征","recheckResult":1,"momOrders":[{"wipOrderNo":"001103030335","wipOrderType":"101.0","partName":"混合空气箱安装M4"}]}’}</flex1:Parameter>
          <flex1:Password>mtdl001</flex1:Password>
            <flex1:Username>123456</flex1:Username>
         </flex:inputs>
      </flex:Invoke>
   </soap:Body>
</soap:Envelope>
'''


def publish_calibration_raw_payload(rid: int, orders: List[MOMOrder], tool_info: ToolsInfo, check: checkValue) -> str:
    data = publish_calibration_payload(rid, orders, tool_info, check)
    ret = f'''
    <soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:del="http://www.apriso.com/DELMIAApriso"
    xmlns:flex="http://schemas.datacontract.org/2004/07/FlexNet.WebServices">
    <soap:Header
        xmlns:wsa="http://www.w3.org/2005/08/addressing">
        <a:To s:mustUnderstand="1"
            xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:a="http://www.w3.org/2005/08/addressing">http://172.31.119.70/Apriso/WebServices/Public/MOM_PeripheralSystem_InspectionInfo.svc?wsdl
        </a:To>
        <wsa:Action>http://www.apriso.com/DELMIAApriso/MOM_PeripheralSystem_InspectionInfo/Invoke</wsa:Action>
    </soap:Header>
    <soap:Body>
        <del:Invoke>
            <!--Optional:-->
            <del:inputs>
                <!--Optional:-->
                <!--Optional:-->
                <flex:Parameter>{json.dumps(data)}</flex:Parameter>
                <flex:Password>123456</flex:Password>
                <flex:Username>mtdl001</flex:Username>
            </del:inputs>
        </del:Invoke>
    </soap:Body>
</soap:Envelope>
    '''
    logger.debug("原始数据包: {}".format(pformat(ret, indent=4)))
    return ret


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
        "Parameter": json.dumps(param)
    }


def publish_calibration_value_2_mom_wsdl(conn: Connection, tool_sn: str, orders: List[MOMOrder],
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
    if raw:
        return publish_calibration_raw_payload(rid, orders, tool_info, check)
    payload = publish_calibration_payload(rid, orders, tool_info, check)
    return payload
