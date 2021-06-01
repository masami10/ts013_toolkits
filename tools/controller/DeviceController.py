# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
import os
from qasync import QEventLoop
import asyncio
from transport.http_server import HttpServer
from transport.tcp_client import TcpClient
from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QPushButton, QRadioButton, QTableWidget

from ..view import window as main_window
import pandas as pd
from loguru import logger


def is_config_valid(config):
    return True


class DeviceController:
    _client: TcpClient
    _config: dict

    def __init__(self, window: main_window.ToolKitWindow):
        self.window = window
        self.notify = self.window.notify_box
        self._config = {}
        ui = self.window.ui
        ui.DeviceConnectButton.clicked.connect(self.device_connect)
        ui.DeviceDisconnectButton.clicked.connect(self.device_disconnect)
        self.window.device_config_group.inputChanged.connect(self.on_config_input)
        self.render(False)
        self.device_connect()

    def on_config_input(self, key, value):
        self._config.update({
            key: value
        })

    # 0004 10/02/21 08:34:54 21.9    0.00     A
    def client_log(self, msg):
        dd = msg.split(' ')
        data = list(filter(lambda d: d != '', dd))
        count, date, time, torque, angle, result = data
        logger.info(f'接收到标定数据: {count} {date}, {time}, {torque}, {angle}, {result} ')
        self.notify.info(msg)

    def get_client_config(self):
        return {
            **self._config,
            'newline': '\r\n'
        }

    def _start_client(self):
        config = self.get_client_config()
        if not is_config_valid(config):
            raise Exception('TCP配置错误')
        self._client = TcpClient(**config)
        self._client.set_handler(self.client_log)
        self._client.start(self.on_client_start)

    def on_client_start(self):
        self.render(True)

    def _stop_client(self):
        self._client.stop()

    def device_connect(self):
        try:
            self.notify.info(
                '正在连接标定设备(tcp://{}:{})...'.format(self._config.get('ip', ''), self._config.get('port', '')))
            self._start_client()
        except Exception as e:
            self.notify.error('连接标定设备失败：')
            self.notify.error(repr(e))

    def device_disconnect(self):
        self.notify.info('正在断开标定设备...')
        # todo: 实现设备断开
        self._stop_client()
        self.render(False)

    def render(self, status: bool):
        self.window.DeviceConnStatusIndicator.set_success(status)
        self.window.HomeDeviceConnStatusIndicator.set_success(status)
