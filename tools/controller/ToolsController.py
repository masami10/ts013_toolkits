# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
import os
from qasync import QEventLoop
import asyncio
from transport.http_server import HttpDaemon
from transport.tcp_client import TcpClient
from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QPushButton, QRadioButton, QTableWidget

from ..view import window as main_window
import pandas as pd
from loguru import logger


def remove_tool_button(tool_sn, on_click):
    t = QPushButton()
    t.setProperty('class', 'smallButton')

    def on_button_clicked():
        on_click(tool_sn)

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

    def __init__(self, window: main_window.ToolKitWindow):
        self.window = window
        self.notify = self.window.notify_box
        self.content = pd.DataFrame({
            '定检编号': ['tool1', 'tool2'],
            '分类号': ['code1', 'code2'],
            '物料号': ['proda', 'prodb'],
            '名称': ['namea', 'nameb'],
            '规格': ['speca', 'specb'],
            'RFID': ['rfida', 'rfidb']
        })  # fixme
        self.render()

    def add_tool(self):
        self.notify.info('新增工具')
        self.render()

    def render_tools_config_table(self):
        tools = list(self.content['定检编号'])
        content = pd.DataFrame({
            '定检编号': tools,
            '分类号': list(self.content['分类号']),
            '物料号': list(self.content['物料号']),
            '名称': list(self.content['名称']),
            '规格': list(self.content['规格']),
            'RFID': list(self.content['RFID']),
            '动作': list(map(lambda tool: remove_tool_button(tool, self.notify.info), tools))
        })
        self.window.tools_config_table.render(content)
        table: QTableWidget = self.window.tools_config_table
        for row in range(len(tools)):
            table.setRowHeight(row, 50)

    def render_tools_pick_table(self):
        tools = list(self.content['定检编号'])
        content = pd.DataFrame({
            '定检编号': tools,
            '选中': list(map(lambda tool: select_tool_radio(tool, self.notify.info), tools))
        })
        self.window.tools_table.render(content)

    def render(self):
        self.render_tools_config_table()
        self.render_tools_pick_table()

    def remove_tool(self):
        # todo: do remove
        self.render()

    def tool_content_edit(self, tool, key, value):
        # todo: do edit
        self.render()
