from typing import Any, Dict, Optional, List
from py_singleton import singleton
from store.types import ToolsInfo, checkValue, MOMOrder, ToolsTorqueInfo
from loguru import logger
from sqlite3 import Connection
from store.config import Config
from api.restful_api import request_get_tool_info
from http import HTTPStatus


@singleton
class StorageData(object):

    def init_tools(self, setting: Config):
        tools_config = setting.tools_config
        for c in tools_config:
            self.add_tool(**c)

    def set_connection(self, conn: Connection):
        self._connect = conn

    def __init__(self, conn: Optional[Connection] = None):
        self._data = {'tools': {}, 'checkResult': checkValue(0.0)}
        self._connect = conn

    def _update_data(self, key: str, value: Any):
        self._data.update({key: value})

    def update_inputs_data(self, key: str, val: Any):
        self._data.get('inputs', {}).update({key: val})
        if key == 'targetTorque':
            self.checkResult.targetValue = float(val)
            return
        if key == 'firstCheckCard':
            self.checkResult.checkPerson.set_number(val)
            return
        if key == 'FirstCheckName':
            self.checkResult.checkPerson.set_name(val)
            return
        if key == 'recheckCard':
            self.checkResult.recheckPerson.set_number(val)
            return
        if key == 'recheckName':
            self.checkResult.recheckPerson.set_name(val)
            return
        if key == 'toolFixedInspectionCode':
            t = self.get_tool_via_inspect_code(val)
            if not t:
                return

    @property
    def checkResult(self) -> checkValue:
        return self._data.get('checkResult')

    def update_check_result_data(self, is_first_check: bool, val: bool):
        result = self.checkResult
        if is_first_check:
            result.setCheckResult(val)
        else:
            result.setReCheckResult(val)

    def get_inputs_data(self):
        return self._data.get('inputs', {})

    def get_data(self, key: str, default=None):
        return self._data.get(key, default)

    def add_tool(self, toolFixedInspectionCode: str, toolClassificationCode: str, toolMaterialCode: str,
                 toolRfid: str, toolName: str, toolSpecificationType: str):
        tool = ToolsInfo(toolFixedInspectionCode, toolClassificationCode, toolMaterialCode, toolRfid, toolName,
                         toolSpecificationType)
        self._data.get('tools', {}).update({
            toolFixedInspectionCode: tool
        })

    def del_tool(self, toolFixedInspectionCode: str):
        try:
            self._data.get('tools', {}).pop(toolFixedInspectionCode)
        except Exception as e:
            logger.error(f'未发现工具: {toolFixedInspectionCode}')

    def edit_tool(self, tool_data: dict):
        ins_code = tool_data.get('toolFixedInspectionCode', None)
        logger.info(f'编辑工具: {ins_code}')
        logger.debug(repr(tool_data))
        if ins_code is None:
            raise Exception('没有指定定检编号')
        tool_info = ToolsInfo(**tool_data)
        entry: Dict = self._data.get('tools', {})
        entry.update({
            ins_code: tool_info
        })
        return entry

    def get_tool_via_inspect_code(self, inspect_code: str) -> Optional[ToolsInfo]:
        data = self.get_tools()
        if not data:
            return None
        return data.get(inspect_code)

    def get_tools(self) -> Dict[str, ToolsInfo]:
        return self._data.get('tools', {})

    def do_generate_tool_torque_info(self, url: str, order: MOMOrder):
        order.toolTorqueInfo = {}
        try:
            success, resp = request_get_tool_info(url, order.partName)
            if not success:
                msg = "request_get_tool_info 调用接口失败: {}".format(resp.text)
                raise Exception(msg)
            data = resp.json()
            if data['status_code'] != HTTPStatus.OK:
                msg = "request_get_tool_info 调用接口失败: {}".format(resp.text)
                raise Exception(msg)
            d: dict = data.get('msg', {})
            if not d:
                return
            val: List
            cache = {}
            for key, val in d.items():
                tools = []
                for v in val:
                    t, tool_inspect_code = v.split(']')
                    t_torque, pset = t.split(',')
                    torque = t_torque[1:]
                    if tool_inspect_code not in cache.keys():
                        cache.update({
                            tool_inspect_code: []
                        })
                    e = cache.get(tool_inspect_code)
                    if torque in e:
                        continue
                    else:
                        e.append(torque)
                    ti = self.get_tool_via_inspect_code(tool_inspect_code)
                    if not ti:
                        logger.error(f"未找到相应的工具: {tool_inspect_code}")
                        continue
                    tti = ToolsTorqueInfo(torque=torque, pset=pset, **ti.__dict__)
                    tools.append(tti)
                order.toolTorqueInfo.update({key: tools})
        except Exception as e:
            raise e

    def __str__(self):
        return 'Global Storage'
