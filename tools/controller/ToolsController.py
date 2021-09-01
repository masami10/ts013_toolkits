# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QRadioButton, QTableWidget
from typing import Dict
from ..view import window as main_window
import pandas as pd
from .ToolsAppendController import ToolsAppendController
from store.store import StorageData
from store.config import Config
from store.types import ToolsInfo
from PyQt5 import QtWidgets
from tools.model.ToolsModel import ToolsModel


def remove_tool_button(tool, on_click):
    t = QPushButton()
    t.setProperty('class', 'smallButton')

    def on_button_clicked():
        on_click(tool)

    t.clicked.connect(on_button_clicked)
    t.setText('删除')
    return t


def select_tool_radio(tool_sn, on_select, selected: bool):
    t = QRadioButton()
    t.setChecked(selected)

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

    def save_tool(self, tool_data: Dict):
        data: Dict[str, ToolsInfo] = self._store.edit_tool(tool_data)
        dd = [tool.__dict__ for tool in data.values()]
        self._config.set_tools_config(dd)
        self.render()

    def edit_tool(self, tool):
        content = ToolsModel().content.set_index('toolFixedInspectionCode')
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
        content = ToolsModel().content
        tools = list(content['toolFixedInspectionCode'])
        content = pd.DataFrame({
            '定检编号': tools,
            '分类号': list(content['toolClassificationCode']),
            '物料号': list(content['toolMaterialCode']),
            '名称': list(content['toolName']),
            '规格': list(content['toolSpecificationType']),
            'RFID': list(content['toolRfid']),
            '动作': list(map(lambda tool: remove_tool_button(tool, self.remove_tool), tools))
        })
        self.window.tools_config_table.table_render_signal.emit(content)
        table: QTableWidget = self.window.tools_config_table
        for row in range(len(tools)):
            table.setRowHeight(row, 50)

    def render_tools_pick_table(self):
        content_current_order = ToolsModel().content_current_order
        tools = list(content_current_order['toolFixedInspectionCode'])
        torques = list(content_current_order['torque'])
        zipped = zip(tools, torques)
        if not tools:
            return
        check_status_map = {
            0: '未标定',
            1: '已初检',
            2: '已复检'
        }
        content = pd.DataFrame({
            '定检编号': tools,
            '程序号': list(content_current_order['pset']),
            '扭矩值': torques,
            '标定状态': list(map(lambda c: check_status_map[c], content_current_order['check_status'])),
            '选中': list(map(lambda tool: select_tool_radio(
                tool,
                self.render_tool_detail,
                ToolsModel().is_selected(*tool)
            ), zipped))
        })
        table = self.window.tools_table
        table.table_render_signal.emit(content)
        header = table.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
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
        tools = ToolsModel().content
        tools = tools.set_index('toolFixedInspectionCode')
        tool, torque = t
        if isinstance(torque, str):
            fTorque = float(torque)
        else:
            fTorque = torque
        minTorque = round(fTorque * 0.975, 2)
        maxTorque = round(fTorque * 1.025, 2)
        tool_selected = dict(tools.loc[tool])
        # 删除界面上没有的字段
        del tool_selected['torque']
        self.window.input_group.set_texts({
            **tool_selected,
            "targetTorque": torque,
            "minTorque": str(minTorque),
            "maxTorque": str(maxTorque),
            'toolFixedInspectionCode': tool
        })
        ToolsModel().set_selected_torque(tool, torque)
        return
