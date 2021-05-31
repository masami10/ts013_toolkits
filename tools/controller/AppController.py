# -*- coding:utf-8 -*-

from .GenTemplController import GenTemplController
from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
import os
from qasync import QEventLoop
import asyncio
from transport.http_server import HttpDaemon
from qt_material import apply_stylesheet
from ..view import window as main_window
from .TemplateCompareController import TemplateCompareController


class AppController:

    def __init__(self):
        # Create the application object
        self.app = QtWidgets.QApplication(sys.argv)

        self._threads = []
        self._http_server = HttpDaemon()

        # Create the form object
        self.window = main_window.ToolKitWindow(self._http_server)
        self.init_controllers()
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

    template_compare_controller: TemplateCompareController = None
    gen_tmpl_controller: GenTemplController = None

    def init_controllers(self):
        self.template_compare_controller = TemplateCompareController(self.window)
        self.gen_tmpl_controller = GenTemplController(self.window)

    def connect_signals(self):
        window = self.window
        ui = window.ui
        ### tab 1 曲线对比
        ui.load_order_btn.clicked.connect(self.template_compare_controller.load_bolt_list)
        ui.submit_btn.clicked.connect(self.template_compare_controller.load_online_template)
        window.input_group.inputChanged.connect(self.on_input)
        window.config_input_group.inputChanged.connect(self.on_config_input)
        window.FirstCheckResultButton.successChanged.connect(self.on_result_success_changed)
        window.RecheckResultButton.successChanged.connect(self.on_result_success_changed)
        ui.DeviceConnectButton.clicked.connect(self.device_connect)
        ui.DeviceDisconnectButton.clicked.connect(self.device_disconnect)

    def on_input(self, key, value):
        self.window.notify_box.info('字段输入：{}，{}'.format(key, value))

    def on_config_input(self, key, value):
        self.window.notify_box.info('配置输入：{}，{}'.format(key, value))

    def on_result_success_changed(self, result_key, success):
        self.window.notify_box.info('结果变化：{}，{}'.format(result_key, success))

    def device_connect(self):
        self.window.notify_box.info('正在连接标定设备...')
        # todo: 实现设备连接
        self.window.DeviceConnStatusIndicator.set_success(True)
        self.window.HomeDeviceConnStatusIndicator.set_success(True)

    def device_disconnect(self):
        self.window.notify_box.info('正在断开标定设备...')
        # todo: 实现设备断开
        self.window.DeviceConnStatusIndicator.set_success(False)
        self.window.HomeDeviceConnStatusIndicator.set_success(False)
