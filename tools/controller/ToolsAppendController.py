# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
import os
from qasync import QEventLoop
import asyncio
from transport.http_server import HttpDaemon
from transport.tcp_client import TcpClient
from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QPushButton, QRadioButton, QTableWidget, QMainWindow

from ..view import window as main_window
from ..view.ToolsAppendWindow import ToolsAppendWindow
import pandas as pd
from loguru import logger


class ToolsAppendController:
    append_window: ToolsAppendWindow
    _content: dict

    def __init__(self, window: main_window.ToolKitWindow):
        self.window = window
        self.notify = self.window.notify_box
        self._content = {}
        self.append_window = self.window.tools_append_window
        self.connect_tools_append_window_signals()
        self.render()

    def connect_tools_append_window_signals(self):
        self.append_window.ui.SaveButton.clicked.connect(self.on_save)
        self.append_window.ui.CancelButton.clicked.connect(self.on_cancel)

    def on_edit(self, key, value):
        self._content.update({
            key: value
        })

    def on_save(self):
        self.close_window()

    def on_cancel(self):
        self.close_window()

    def close_window(self):
        window: QMainWindow = self.append_window.qt_instance
        window.close()

    def create(self):
        self._content = {
            'inspectionCode': '',
            'productCode': '',
            'RFIDEdit': '',
            'classificationCode': '',
            'name': '',
            'specs': '',
        }
        window: QMainWindow = self.append_window.qt_instance
        window.setWindowTitle('添加工具')
        window.show()
        self.render()

    def edit(self, tool: dict):
        self._content = tool
        window: QMainWindow = self.append_window.qt_instance
        window.setWindowTitle('编辑工具')
        self.append_window.qt_instance.show()
        self.render()

    def render(self):
        self.append_window.input_group.set_texts(self._content)
