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


class AppController:

    def __init__(self):
        # Create the application object
        self.app = QtWidgets.QApplication(sys.argv)

        self._threads = []
        self._http_server = HttpDaemon()

        # Create the form object
        self.window = main_window.ToolKitWindow(self._http_server)
        self.connect_signals()
        self.apply_material_theme()
        self.render_tools()
        self.render_results()  # fixme: 移动到产生结果的地方


    # 0004 10/02/21 08:34:54 21.9    0.00     A
    def client_log(self, msg):
        dd = msg.split(' ')
        data = list(filter(lambda d: d != '', dd))
        count, date, time, torque, angle, result = data
        logger.info(f'接收到标定数据: {count} {date}, {time}, {torque}, {angle}, {result} ')
        self.window.notify_box.info(msg)

    def start_client(self):
        try:
            client = TcpClient(
                ip='192.168.3.100',
                port=7000,
                newline='\r\n'
            )
            client.set_handler(self.client_log)
            client.start()
        except Exception as e:
            self.window.notify_box.error(repr(e))

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
        self.window.qt_instance.show()

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
        ui.DeviceConnectButton.clicked.connect(self.device_connect)
        ui.DeviceDisconnectButton.clicked.connect(self.device_disconnect)
        ui.load_order_btn.clicked.connect(self.load_orders)

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

    def load_orders(self):
        self.render_orders()

    def render_orders(self):
        content = pd.DataFrame({
            '订单号': ['1', '2'],
            '已选择': ['a', 'b']
        })
        self.window.order_table.render(content)

    def render_tools(self):
        content = pd.DataFrame({
            '工具序列号': ['1', '2'],
            '已选择': ['a', 'b']
        })
        self.window.tools_table.render(content)

    def render_results(self):
        content = pd.DataFrame({
            '时间': ['2021年5月31日17:35:18', '2021年5月31日17:35:21'],
            '扭矩值': ['12.5', '14.6']
        })
        self.window.result_table.set_inactive()
        self.window.result_table.render(content)
