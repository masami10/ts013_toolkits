from typing import Any, Dict, Optional
from py_singleton import singleton
from store.types import ToolsInfo, checkValue
from loguru import logger
from typing import Dict


@singleton
class StorageData(object):
    def __init__(self):
        self._data = {'tools': {}, 'checkResult': checkValue(0.0), 'selected_tool': {}}

    def _update_data(self, key: str, value: Any):
        self._data.update({key, value})

    def update_inputs_data(self, key: str, val: Any):
        self._data.get('inputs', {}).update({key, val})
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
            self.set_selected_tool(t)

    def set_selected_tool(self, tool: ToolsInfo):
        self._data.update({'selected_tool': tool})

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
