import os
import json
from utils.tools import serialize_obj_2_json
from typing import List
from store.types import MOMOrder, ToolsInfo
from transport.constants import now
from sqlite3 import Connection, Cursor

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


def publish_calibration_payload(conn: Connection, rid: int, orders: List[MOMOrder], tool_info: ToolsInfo):
    return {
        "Parameter": {
            {"MethodName": "TorqueCheckInfo", "Parameter":
                {"id": rid, "toolFixedInspectionCode": tool_info.toolFixedInspectionCode,
                 "toolClassificationCode": tool_info.toolClassificationCode,
                 "toolMaterialCode": "000000001800000181",
                 "toolRfid": "315110040000000000000224", "toolName": tool_info.toolName,
                 "toolSpecificationType": "扭矩范围(4-20)N.m", "checkValue": 55.0,
                 "maxCheckValue": 56.37, "minCheckValue": 53.63, "maxRecheckValue": 57.75,
                 "minRecheckValue": 52.25, "checkTime": "2020-04-2416:27:30",
                 "checkValue1": 55.0, "checkValue2": 55.1, "checkValue3": 55.2,
                 "checkEmployeeNo": "65595", "checkEmployeeName": "朱亚征", "checkResult": 1,
                 "recheckTime": now(), "recheckValue": 55.0,
                 "recheckEmployeeNo": "65595", "recheckEmployeeName": "朱亚征",
                 "recheckResult": 1, "momOrders": serialize_obj_2_json(orders)}}}}


def insert_into_tool_calibration_item(cr: Cursor, identity: str) -> int:
    cr.execute("insert into ts013_wsdl (orders) values (?)", identity)
    return cr.lastrowid


def publish_calibration_value_2_mom_wsdl(conn: Connection, tool_sn: str, orders: List[MOMOrder]):
    ss = [o.wipOrderNo for o in orders]
    str_orders = ",".join(ss)
    identity = f"{tool_sn}@{str_orders}"
    cr = conn.cursor()
    cr.execute("SELECT id from ts013_wsdl where orders = ?", identity)
    result = cr.fetchone()
    if not result:
        rid = insert_into_tool_calibration_item(cr, identity)
    else:
        rid = result[0]
    conn.commit()
    payload = publish_calibration_payload(rid)
