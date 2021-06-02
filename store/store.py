from typing import Any, Dict
from py_singleton import singleton
from store.types import ToolsInfo
from loguru import logger


@singleton
class StorageData(object):
    def __init__(self):
        self._data = {'tools': {}}

    def update_data(self, key: str, value: Any):
        self._data.update({key, value})

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
        logger.info('编辑工具')
        logger.info(repr(tool_data))
        ins_code = tool_data.get('toolFixedInspectionCode', None)
        if ins_code is None:
            raise Exception('没有指定定检编号')
        tool_info = ToolsInfo(**tool_data)
        self._data.get('tools', {}).update({
            ins_code: tool_info
        })

    def get_tools(self) -> Dict[str, ToolsInfo]:
        return self._data.get('tools', {})

    def __str__(self):
        return 'Global Storage'
