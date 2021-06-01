# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
import os
from qasync import QEventLoop
import asyncio
from transport.http_server import HttpDaemon
from transport.tcp_client import TcpClient
from qt_material import apply_stylesheet
from ..view import window as main_window
import pandas as pd
from loguru import logger
from .ToolsController import ToolsController
from .DeviceController import DeviceController
from .OrderController import OrderController
from store.store import StorageData


class AppController:

    def __init__(self):
        # Create the application object
        self.app = QtWidgets.QApplication(sys.argv)

        self._threads = []
        self._http_server = HttpDaemon()

        self.glb_storage = StorageData()  # 单例模式

        # Create the form object
        self.window = main_window.ToolKitWindow(self._http_server)
        self.notify = self.window.notify_box
        self._tools_controller = ToolsController(self.window)
        self._device_controller = DeviceController(self.window)
        self._order_controller = OrderController(self.window)

        self.connect_signals()
        self.apply_material_theme()

    def apply_material_theme(self):
        extra = {
            # Button colors
            'danger': '#dc3545',
            'warning': '#ffc107',
            'success': '#66bb6a',

            # Font
            'font-family': 'Roboto',
        }

        apply_stylesheet(self.app, theme='light_blue.xml', extra=extra)
        stylesheet = self.app.styleSheet()
        with open('styles/custom.css') as file:
            self.app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    def run_app(self):
        loop = QEventLoop()
        asyncio.set_event_loop(loop)
        # Show form
        self.window.show()

        # Run the program
        sys.exit(self.app.exec())

    def connect_signals(self):
        window = self.window
        ui = window.ui
        ### tab 1 曲线对比
        window.input_group.inputChanged.connect(self.on_input)
        window.config_input_group.inputChanged.connect(self.on_config_input)
        window.FirstCheckResultButton.successChanged.connect(self.on_result_success_changed)
        window.RecheckResultButton.successChanged.connect(self.on_result_success_changed)
        ui.ToolsConfigAddButton.clicked.connect(self._tools_controller.add_tool)

    def on_input(self, key, value):
        self.notify.info('字段输入：{}，{}'.format(key, value))

    def on_config_input(self, key, value):
        self.notify.info('配置输入：{}，{}'.format(key, value))

    def on_result_success_changed(self, result_key, success):
        self.notify.info('结果变化：{}，{}'.format(result_key, success))