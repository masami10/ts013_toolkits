# -*- coding:utf-8 -*-
from transport.tcp_client import TcpClient
from ..view import window as main_window
import pandas as pd
from loguru import logger


def is_config_valid(config):
    if config.get('ip', None) is None:
        raise Exception('ip未指定')
    if config.get('port', None) is None:
        raise Exception('端口未指定')
    return True


class DeviceController:
    _client: TcpClient
    _config: dict
    _results: pd.DataFrame

    def __init__(self, window: main_window.ToolKitWindow):
        self.window = window
        self.notify = self.window.notify_box
        self._config = {}
        ui = self.window.ui
        self._results = pd.DataFrame({
            'count': [],
            'date': [],
            'time': [],
            'torque': [],
            'angle': [],
            'result': []
        })
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
    def handle_result(self, msg):
        self.notify.info('收到标定结果')
        self.notify.info(msg)
        dd = msg.split(' ')
        data = list(filter(lambda d: d != '', dd))
        count, date, time, torque, angle, result = data
        logger.info(f'接收到标定数据: {count} {date}, {time}, {torque}, {angle}, {result} ')
        self._results = self._results.append(pd.DataFrame({
            'count': [count],
            'date': [date],
            'time': [time],
            'torque': [torque],
            'angle': [angle],
            'result': [result]
        }), ignore_index=True)
        self.render_results()

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
        self._client.set_handler(self.handle_result)
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
        self._stop_client()
        self.render(False)

    def render(self, status: bool):
        self.window.DeviceConnStatusIndicator.set_success(status)
        self.window.HomeDeviceConnStatusIndicator.set_success(status)

    def render_results(self):
        content = pd.DataFrame({
            '时间': list(self._results['time']),
            '扭矩值': list(self._results['torque']),
            '角度值': list(self._results['angle'])
        })
        self.window.result_table.render(content)
