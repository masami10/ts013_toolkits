from typing import Any, List
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

    def get_tools(self) -> List[ToolsInfo]:
        return self._data.get('tools', {})

    def __str__(self):
        return 'Global Storage'
