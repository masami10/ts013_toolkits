# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QRadioButton, QTableWidget
from typing import Dict, List
from ..view import window as main_window
import pandas as pd
from .ToolsAppendController import ToolsAppendController
from store.store import StorageData
from store.config import Config
from store.types import ToolsInfo, ToolsTorqueInfo
from PyQt5 import QtWidgets


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
        tools = self._store.get_tools()
        tdf = pd.DataFrame({
            'toolFixedInspectionCode': [],
            'toolMaterialCode': [],
            'toolRfid': [],
            'toolClassificationCode': [],
            'toolName': [],
            'toolSpecificationType': [],
            'torque': []
        })
        for key, value in tools.items():
            tdf = tdf.append(value.to_dict, ignore_index=True)
        return tdf

    @property
    def content_current_order(self):
        tdf = pd.DataFrame({
            'toolFixedInspectionCode': [],
            'toolMaterialCode': [],
            'toolRfid': [],
            'toolClassificationCode': [],
            'toolName': [],
            'toolSpecificationType': [],
            'torque': [],
            'pset': []
        })
        select_orders = self._store.selected_orders
        if not select_orders:
            return tdf
        order = select_orders[0]
        tools: List[ToolsTorqueInfo] = []
        for k, v in order.toolTorqueInfo.items():
            tools.extend(v)

        for toolTorqueInfo in tools:
            d = toolTorqueInfo.to_dict
            tdf = tdf.append(pd.DataFrame(d), ignore_index=True)
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
        self.window.tools_config_table.table_render_signal.emit(content)
        table: QTableWidget = self.window.tools_config_table
        for row in range(len(tools)):
            table.setRowHeight(row, 50)

    def render_tools_pick_table(self):
        tools = list(self.content_current_order['toolFixedInspectionCode'])
        torques = list(self.content_current_order['torque'])
        zipped = zip(tools, torques)
        if not tools:
            return
        content = pd.DataFrame({
            '定检编号': tools,
            '程序号': list(self.content_current_order['pset']),
            '扭矩值': list(self.content_current_order['torque']),
            '选中': list(map(lambda tool: select_tool_radio(tool, self.render_tool_detail), zipped))
        })
        table = self.window.tools_table
        table.table_render_signal.emit(content)
        header = table.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        for row in range(len(tools)):
            table.setRowHeight(row, 50)

    def render(self):
        self.render_tools_config_table()
        self.render_tools_pick_table()

    def remove_tool(self, tool_inspect_code: str):
        self._store.del_tool(tool_inspect_code)
        self._config.del_tool_config(tool_inspect_code)
        self.render()

    def render_tool_detail(self, t: tuple):
        tools = self.content
        tools = tools.set_index('toolFixedInspectionCode')
        tool, torque = t
        fTorque = 0.0
        if isinstance(torque, str):
            fTorque = float(torque)
        minTorque = round(fTorque * 0.975, 2)
        maxTorque = round(fTorque * 1.025, 2)
        tool_selected = dict(tools.loc[tool])
        self.window.input_group.set_texts({
            **tool_selected,
            "targetTorque": torque,
            "minTorque": str(minTorque),
            "maxTorque": str(maxTorque),
            'toolFixedInspectionCode': tool
        })
        self._store.set_selected_tool(tool)
        return
