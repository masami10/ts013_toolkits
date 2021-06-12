# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QRadioButton, QTableWidget
from typing import Dict, List
from ..view import window as main_window
import pandas as pd
from .ToolsAppendController import ToolsAppendController
from store.store import StorageData
from store.config import Config
from store.types import ToolsInfo, ToolsTorqueInfo
from itertools import chain


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

    def __init__(self, window: main_window.ToolKitWindow, config: Config, store: StorageData):
        self.window = window
        self.notify = self.window.notify_box
        self._config = config
        self._store = store
        self.append_controller = ToolsAppendController(self.window, self.save_tool)
        self.window.tools_config_table.row_clicked_signal.connect(self.edit_tool)
        self.render()

    @property
    def content(self) -> pd.DataFrame:
        tdf = pd.DataFrame({
            'toolFixedInspectionCode': [],
            'toolMaterialCode': [],
            'toolRfid': [],
            'toolClassificationCode': [],
            'toolName': [],
            'toolSpecificationType': [],
            'torque': []
        })
        select_orders = self._store.selected_orders
        if not select_orders:
            return tdf
        order = select_orders[0]
        tools: List[ToolsTorqueInfo] = []
        for k, v in order.toolTorqueInfo.items():
            tools.extend(v)

        for toolTorqueInfo in tools:
            tdf = tdf.append(toolTorqueInfo.to_dict, ignore_index=True)
        return tdf

    def save_tool(self, tool_data: Dict):
        data: Dict[str, ToolsInfo] = self._store.edit_tool(tool_data)
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
            '扭矩值': list(self.content['torque']),
            '选中': list(map(lambda tool: select_tool_radio(tool, self.render_tool_detail), tools))
        })
        self.window.tools_table.render_table(content)
        table = self.window.tools_table
        for row in range(len(tools)):
            table.setRowHeight(row, 50)

    def render(self):
        self.render_tools_config_table()
        self.render_tools_pick_table()

    def remove_tool(self, tool_inspect_code: str):
        self._store.del_tool(tool_inspect_code)
        self._config.del_tool_config(tool_inspect_code)
        self.render()

    def render_tool_detail(self, tool: str):
        tools = self.content
        tools = tools.set_index('toolFixedInspectionCode')
        tool_selected = dict(tools.loc[tool])
        self.window.input_group.set_texts({
            **tool_selected,
            'toolFixedInspectionCode': tool
        })
        self._store.set_selected_tool(tool)
        return
