from typing import Any, Dict, Optional
from py_singleton import singleton
from store.types import ToolsInfo, checkValue
from store.sql import query_ts013_order_via_codes
from loguru import logger
from typing import Dict
from sqlite3 import Connection
from store.config import Config


@singleton
class StorageData(object):

    def init_tools(self, setting: Config):
        tools_config = setting.tools_config
        for c in tools_config:
            self.add_tool(**c)

    def set_connection(self, conn: Connection):
        self._connect = conn

    def __init__(self, conn: Optional[Connection] = None):
        self._data = {'tools': {}, 'checkResult': checkValue(0.0), 'selected_tool': {}, 'selected_orders': []}
        self._connect = conn

    def _update_data(self, key: str, value: Any):
        self._data.update({key: value})

    def update_selected_orders(self, orders_str: str):
        orders = []
        if orders_str == "":
            self._data.update({'selected_orders': []})
        else:
            order_codes = orders_str.split(',')
            orders = query_ts013_order_via_codes(self._connect, order_codes)
        self._data.update({'selected_orders': orders})

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

    def set_selected_tool(self, tool_inspect_code: str):
        t = self.get_tool_via_inspect_code(tool_inspect_code)
        if not t:
            return
        self._data.update({'selected_tool': t})

    @property
    def selected_orders(self):
        return self._data.get('selected_orders')

    @property
    def selected_tool(self) -> Optional[ToolsInfo]:
        return self._data.get('selected_tool')

    @property
    def checkResult(self) -> checkValue:
        return self._data.get('checkResult')

    def update_check_result_data(self, result_key: str, val: bool):
        result = self.checkResult
        if result_key == 'firstCheckResult':
            result.setCheckResult(val)
        if result_key == 'recheckResult':
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

    def __str__(self):
        return 'Global Storage'
