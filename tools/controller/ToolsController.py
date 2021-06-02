# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QRadioButton, QTableWidget
from typing import Dict
from ..view import window as main_window
import pandas as pd
from .ToolsAppendController import ToolsAppendController
from store.store import StorageData
from store.config import Config
from store.types import ToolsInfo

store = StorageData()


def remove_tool_button(tool, on_click):
    t = QPushButton()
    t.setProperty('class', 'smallButton')

    def on_button_clicked():
        on_click(tool)

    t.clicked.connect(on_button_clicked)
    t.setText('删除')
    return t


def select_tool_radio(tool_sn, on_select):
    t = QRadioButton()

    def on_button_clicked():
        on_select(tool_sn)

    t.clicked.connect(on_button_clicked)
    t.setText('')
    return t


class ToolsController:
    append_controller: ToolsAppendController

    def __init__(self, window: main_window.ToolKitWindow, config: Config):
        self.window = window
        self.notify = self.window.notify_box
        self._config = config
        self.append_controller = ToolsAppendController(self.window, self.save_tool)
        self.window.tools_config_table.row_clicked_signal.connect(self.edit_tool)
        self.render()

    @property
    def content(self) -> pd.DataFrame:
        tools = store.get_tools()
        tdf = pd.DataFrame({
            'toolFixedInspectionCode': [],
            'toolMaterialCode': [],
            'toolRfid': [],
            'toolClassificationCode': [],
            'toolName': [],
            'toolSpecificationType': [],
        })
        for key, value in tools.items():
            tdf = tdf.append(value.to_dict, ignore_index=True)
        return tdf

    def save_tool(self, tool_data: Dict):
        data: Dict[str, ToolsInfo] = store.edit_tool(tool_data)
        dd = [tool.__dict__ for tool in data.values()]
        self._config.set_tools_config(dd)
        self.render()

    def edit_tool(self, tool):
        content = self.content.set_index('toolFixedInspectionCode')
        tool_data = dict(content.loc[tool])
        self.append_controller.edit({
            **tool_data,
            'toolFixedInspectionCode': tool
        })

    def add_tool(self):
        self.notify.info('新增工具')
        self.append_controller.create()
        self.render()

    def render_tools_config_table(self):
        tools = list(self.content['toolFixedInspectionCode'])
        content = pd.DataFrame({
            '定检编号': tools,
            '分类号': list(self.content['toolClassificationCode']),
            '物料号': list(self.content['toolMaterialCode']),
            '名称': list(self.content['toolName']),
            '规格': list(self.content['toolSpecificationType']),
            'RFID': list(self.content['toolRfid']),
            '动作': list(map(lambda tool: remove_tool_button(tool, self.remove_tool), tools))
        })
        self.window.tools_config_table.render_table(content)
        table: QTableWidget = self.window.tools_config_table
        for row in range(len(tools)):
            table.setRowHeight(row, 50)

    def render_tools_pick_table(self):
        tools = list(self.content['toolFixedInspectionCode'])
        content = pd.DataFrame({
            '定检编号': tools,
            '选中': list(map(lambda tool: select_tool_radio(tool, self.render_tool_detail), tools))
        })
        self.window.tools_table.render_table(content)

    def render(self):
        self.render_tools_config_table()
        self.render_tools_pick_table()

    def remove_tool(self, tool):
        store.del_tool(tool)
        # todo: do remove
        self.render()

    def render_tool_detail(self, tool):
        tools = self.content
        tools = tools.set_index('toolFixedInspectionCode')
        tool_selected = dict(tools.loc[tool])
        self.window.input_group.set_texts({
            **tool_selected,
            'toolFixedInspectionCode': tool
        })
        return
