# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
import os
from qasync import QEventLoop
import asyncio
from transport.http_server import HttpServer
from store.config import Config
from qt_material import apply_stylesheet
from ..view import window as main_window
from .ToolsController import ToolsController
from .DeviceController import DeviceController
from .OrderController import OrderController
from .ConnectionController import ConnectionController
from store.store import StorageData
from store.contants import TS013_DB_NAME
import sqlite3
from typing import Any
from loguru import logger
from api.wsdl import publish_calibration_value_2_mom_wsdl

TRANSLATION_MAP = {
    'recheckResult': '复检结果',
    'firstCheckResult': '检验结果',
    'True': '成功',
    'False': '失败',
}


def get_translation(v: str):
    default = v
    return TRANSLATION_MAP.get(v, default)


class AppController:

    def __init__(self):
        # Create the application object
        self.app = QtWidgets.QApplication(sys.argv)

        self._db_connect = sqlite3.connect(TS013_DB_NAME)

        self._threads = []
        self._http_server = HttpServer()
        self.glb_config = Config()

        self.glb_storage = StorageData()  # 单例模式
        self.glb_storage.set_connection(self._db_connect)
        self.glb_storage.init_tools(self.glb_config)

        self._cache_data = {"inputs": {}, "results": {}}  # input 和result缓存数据

        # Create the form object
        self.window = main_window.ToolKitWindow(self._http_server)
        self.notify = self.window.notify_box
        self._tools_controller = ToolsController(self.window, self.glb_config, self.glb_storage)
        self._device_controller = DeviceController(self.window, self.glb_storage, self.glb_config)
        self._order_controller = OrderController(self.window, self._db_connect, self.glb_storage)
        self._connection_controller = ConnectionController(self.window, self.glb_config)

        self.window.ui.submit_btn.clicked.connect(self.on_result_submit)

        self.init_sqlite_db()

        self.connect_signals()
        self.apply_material_theme()

    def on_result_submit(self):
        msg = "提交标定数据"
        self.notify.info(msg)
        inputs: dict = self._cache_data.get("inputs")
        for key, val in inputs.items():
            self.glb_storage.update_inputs_data(key, val)
        results: dict = self._cache_data.get("results")
        for key, val in results.items():
            self.glb_storage.update_check_result_data(key, val)

        selected_tool = self.glb_storage.selected_tool
        selected_orders = self.glb_storage.selected_orders
        check = self.glb_storage.checkResult
        publish_calibration_value_2_mom_wsdl(self._db_connect,
                                             selected_tool.toolFixedInspectionCode, selected_orders, selected_tool,
                                             check)

    def update_inputs_cache_data(self, key: str, val: Any):
        entry = self._cache_data.get("inputs")
        entry.update({key: val})

    def update_results_cache_data(self, key: str, val: Any):
        entry = self._cache_data.get("results")
        entry.update({key: val})

    def init_sqlite_db(self):
        if self._db_connect:
            cr = self._db_connect.cursor()
            cr.execute(
                '''CREATE TABLE IF NOT EXISTS ts013_wsdl(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, orders TEXT)''')
            cr.execute(
                '''CREATE TABLE IF NOT EXISTS ts013_orders(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, schedule_date TIMESTAMP,order_no TEXT, order_type TEXT, finished_product_no TEXT)''')
            self._db_connect.commit()
            cr.close()

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
        window.FirstCheckResultButton.successChanged.connect(self.on_result_success_changed)
        window.RecheckResultButton.successChanged.connect(self.on_result_success_changed)
        ui.ToolsConfigAddButton.clicked.connect(self._tools_controller.add_tool)

    def on_input(self, key: str, value: Any):
        self.notify.debug('字段输入：{}，{}'.format(key, value))
        self.update_inputs_cache_data(key, value)
        # self.glb_storage.update_inputs_data(key, value)

    def on_result_success_changed(self, result_key: str, success: bool):
        lvl = 'info'
        if not success:
            lvl = 'error'
        m = getattr(self.notify, lvl, self.notify.info)
        m('结果变化：{}，{}'.format(get_translation(result_key), get_translation(str(success))))
        self.update_results_cache_data(result_key, success)
        # self.glb_storage.update_check_result_data(result_key, success)  # 更新存储的数据
