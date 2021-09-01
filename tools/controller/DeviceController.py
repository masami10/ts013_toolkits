# -*- coding:utf-8 -*-

from transport.tcp_client import TcpClient
from ..view import window as main_window
import pandas as pd
from loguru import logger
from store.config import Config
from store.store import StorageData
from tools.model.InputModel import input_model_instance as input_model
from tools.model.CheckResultModel import check_result_model_instance as result_model


def is_config_valid(config):
    if config.get('ip', None) is None:
        raise Exception('ip未指定')
    if config.get('port', None) is None:
        raise Exception('端口未指定')
    return True


class DeviceController:
    _client: TcpClient

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
        ui.DeviceConnectButton.clicked.connect(self.device_connect)
        ui.DeviceDisconnectButton.clicked.connect(self.device_disconnect)
        self.window.device_config_group.inputChanged.connect(self.on_config_input)
        self.window.ui.ClearResultsButton.clicked.connect(self.clear_results)
        self.window.closeSignal.connect(self.device_disconnect)
        self._client = None
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

    def clear_results(self):
        result_model.clear_results()
        self._store.checkResult.set_measures([])
        self.render_results()

    # 0004 10/02/21 08:34:54 21.9    0.00     A
    def handle_result(self, msg):
        try:
            if not msg:
                return
            self.notify.info('收到标定结果')
            self.notify.info(msg)
            dd = msg.split(' ')
            data = list(filter(lambda d: d != '', dd))
            try:
                count, date, time, torque, angle, result, *rest = data
            except ValueError:
                # 标定仪不支持角度
                count, date, time, torque, result, *rest = data
                angle = None
            logger.info(f'接收到标定数据: {count} {date}, {time}, {torque}, {angle}, {result} ')
            result_model.append_result(count, date, time, torque, angle, result)
            self._store.checkResult.update_measure(torque)  # 将扭矩值存储
            self.render_results()
        except Exception as e:
            self.notify.error(repr(e))

    def get_client_config(self):
        return {
            **self.config,
            'newline': '\r\n'
        }

    def _start_client(self):
        if self._client:
            try:
                self.device_disconnect()
            except Exception as e:
                self.notify.error(e)
            self.notify.info('正在重新连接...')
        config = self.get_client_config()
        if not is_config_valid(config):
            raise Exception('TCP配置错误')
        self.notify.info('正在配置客户端...')

        self._client = TcpClient(**config)
        self.notify.info('正在绑定结果处理程序...')
        self._client.set_handler(self.handle_result)
        self.notify.info('正在启动客户端...')
        self._client.start(self.on_client_status, self.notify)

    def on_client_status(self, status=True):
        self.render(status)

    def _stop_client(self):
        if self._client:
            self._client.stop()
        self._client = None

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
        results = result_model.results
        max_torque = input_model.get_input('maxTorque')
        min_torque = input_model.get_input('minTorque')
        content = pd.DataFrame({
            '时间': list(results['time']),
            '扭矩值': list(results['torque']),
            '角度值': list(results['angle']),
            'mark_error': list(map(
                lambda t: result_model.is_result_nok(t, max_torque, min_torque),
                results['torque']
            ))
        })
        self.window.result_table.table_render_signal.emit(content)
