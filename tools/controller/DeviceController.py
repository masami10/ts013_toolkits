# -*- coding:utf-8 -*-

from transport.tcp_client import TcpClient
from ..view import window as main_window
import pandas as pd
from loguru import logger
from store.config import Config
from store.store import StorageData


def is_config_valid(config):
    if config.get('ip', None) is None:
        raise Exception('ip未指定')
    if config.get('port', None) is None:
        raise Exception('端口未指定')
    return True


class DeviceController:
    _client: TcpClient
    _results: pd.DataFrame

    _config_key_map = {
        'ip': 'device_ip',
        'port': 'device_port'
    }

    def __init__(self, window: main_window.ToolKitWindow, store: StorageData, config: Config):
        self.window = window
        self._store = store
        self._config = config
        self.notify = self.window.notify_box
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

    @property
    def config(self):
        config = {}
        for key, value in self._config_key_map.items():
            config.update({
                key: self._config.get_config(value)
            })
        return config

    def on_config_input(self, key, value):
        if self.config.get(key, None) == value:
            return
        config_key = self._config_key_map.get(key, None)
        if config_key is None:
            raise Exception('无效的配置{}'.format(key))
        self._config.set_config(config_key, value)

    # 0004 10/02/21 08:34:54 21.9    0.00     A
    def handle_result(self, msg):
        self.notify.info('收到标定结果')
        self.notify.info(msg)
        dd = msg.split(' ')
        data = list(filter(lambda d: d != '', dd))
        count, date, time, torque, angle, result, *rest = data
        logger.info(f'接收到标定数据: {count} {date}, {time}, {torque}, {angle}, {result} ')
        self._results = self._results.append(pd.DataFrame({
            'count': [count],
            'date': [date],
            'time': [time],
            'torque': [torque],
            'angle': [angle],
            'result': [result]
        }), ignore_index=True)
        self._store.checkResult.update_measure(torque)  # 将扭矩值存储
        self.render_results()

    def get_client_config(self):
        return {
            **self.config,
            'newline': '\r\n'
        }

    def _start_client(self):
        config = self.get_client_config()
        if not is_config_valid(config):
            raise Exception('TCP配置错误')
        self.notify.info('正在配置客户端...')
        self._client = TcpClient(**config)
        self.notify.info('正在绑定结果处理程序...')
        self._client.set_handler(self.handle_result)
        self.notify.info('正在启动客户端...')
        self._client.start(self.on_client_start, self.notify)

    def on_client_start(self):
        self.render(True)

    def _stop_client(self):
        self._client.stop()

    def device_connect(self):
        try:
            ip = self.config.get('ip', '')
            port = self.config.get('port', '')
            if not ip or not port:
                raise Exception('未设置标定设备IP或端口!!!')
            self.notify.info(
                f'正在连接标定设备(tcp://{ip}:{port})...')
            self._start_client()
        except Exception as e:
            self.notify.error('连接标定设备失败：')
            self.notify.error(str(e))

    def render_config(self):
        self.window.device_config_group.set_texts(self.config)

    def device_disconnect(self):
        self.notify.info('正在断开标定设备...')
        self._stop_client()
        self.render(False)

    def render(self, status: bool):
        self.render_config()
        self.window.DeviceConnStatusIndicator.set_success(status)
        self.window.HomeDeviceConnStatusIndicator.set_success(status)

    def render_results(self):
        content = pd.DataFrame({
            '时间': list(self._results['time']),
            '扭矩值': list(self._results['torque']),
            '角度值': list(self._results['angle'])
        })
        self.window.result_table.render_table(content)
