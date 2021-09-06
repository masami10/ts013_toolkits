# -*- coding:utf-8 -*-
import copy
import json

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
from store.types import MOMOrder
from typing import Any, List
from transport.wsdl import WSDLClient
from pprint import pformat
from api.wsdl import publish_calibration_value_2_mom_wsdl
from api.mes import publish_calibration_value_2_mes_wsdl
from api.restful_api import request_mom_data, request_mes_data
from tools.model.InputModel import input_model_instance
from tools.model.CheckTypeModel import check_type_model_instance
from tools.model.CheckResultModel import check_result_model_instance as result_model
from tools.view.CheckTypeRadio import CheckTypeRadio
from store.sql import DEFAULT_CONNECTION, create_torque_check_status_table
from tools.model.OrdersModel import OrdersModel
from tools.model.ToolsModel import ToolsModel
from store.sql import save_torque_check_status
from transport.constants import now

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

        self._db_connect = DEFAULT_CONNECTION

        self._threads = []
        self._http_server = HttpServer()
        self.glb_config = Config()

        self.glb_storage = StorageData()  # 单例模式
        self.glb_storage.set_connection(self._db_connect)
        self.glb_storage.init_tools(self.glb_config)

        self._wsdl_client = WSDLClient(self._db_connect, self.glb_config.wsdl_base_url)

        # Create the form object
        self.window = main_window.ToolKitWindow(self._http_server)
        self.notify = self.window.notify_box
        self._tools_controller = ToolsController(self.window, self.glb_config, self.glb_storage)
        self._device_controller = DeviceController(self.window, self.glb_storage, self.glb_config)
        self._order_controller = OrderController(self.window, self._db_connect, self.glb_storage, self.glb_config)
        self._connection_controller = ConnectionController(self.window, self.glb_config)
        self._check_type_radio = CheckTypeRadio(
            self.window.ui.firstCheckRadio,
            self.window.ui.recheckRadio
        )
        self.window.ui.submit_btn.clicked.connect(self.on_result_submit)

        self.init_sqlite_db()

        self.connect_signals()
        self.apply_material_theme()

    def on_result_submit(self):
        try:
            if not check_type_model_instance.did_set:
                raise Exception('请选择标定类型！')
            self.notify.info("提交标定数据")
            A = check_type_model_instance
            for key, val in input_model_instance.inputs.items():
                self.glb_storage.update_inputs_data(key, val)
            self.glb_storage.update_inputs_data('firstCheckCard', self.glb_config.get_config('originPersonCode'))
            self.glb_storage.update_inputs_data('FirstCheckName', self.glb_config.get_config('originPersonName'))
            self.glb_storage.update_inputs_data('recheckCard', self.glb_config.get_config('recheckPersonCode'))
            self.glb_storage.update_inputs_data('recheckName', self.glb_config.get_config('recheckPersonName'))

            selected_torque = ToolsModel().selected_torque
            # store\types.py 中dict函数ret.pop('toolTorqueInfo') 会将对象改变，需要先深度拷贝
            selected_orders = copy.deepcopy(OrdersModel().selected_orders)
            if selected_torque is None:
                raise Exception('无法提交：未选中工具')
            if selected_orders is None or len(selected_orders) == 0:
                raise Exception('无法提交：未选中工单')

            if check_type_model_instance.is_first_check:
                result = result_model.results_all_ok(
                    input_model_instance.get_input("maxTorque"),
                    input_model_instance.get_input("minTorque"),
                )
                if not result:
                    raise Exception('无法提交：初检必须满足连续三次成功方可提交')
                self.glb_storage.update_check_result_data(
                    check_type_model_instance.is_first_check,
                    result
                )
            else:
                result = result_model.results_last_ok(
                    input_model_instance.get_input("maxTorque"),
                    input_model_instance.get_input("minTorque"),
                )
                if not result:
                    raise Exception('无法提交：复检必须满足最新一次成功方可提交')
                self.glb_storage.update_check_result_data(
                    check_type_model_instance.is_first_check,
                    result
                )

            check = self.glb_storage.checkResult
            payload = publish_calibration_value_2_mes_wsdl(
                self._db_connect,
                selected_torque.toolFixedInspectionCode,
                selected_orders,
                selected_torque,
                check,
                False
            )
            resultUp = {
                "firstCheck": check_type_model_instance.is_first_check,
                "checkTime": now(),
                "result": check.get_dict(),
                "payload": payload,
            }
            # self.notify.info(json.dumps(resultUp))
            full_url = self.glb_config.wsdl_base_url.split('?')[0]
            success, text = request_mes_data(full_url, data=json.dumps(resultUp))
            if not success:
                raise Exception(text)
            self.notify.info(text)
            save_torque_check_status(
                selected_torque.toolFixedInspectionCode,
                selected_torque.torque,
                check_type_model_instance.is_first_check
            )
            self._order_controller.render()
            self._tools_controller.render_tools_pick_table()
        except Exception as e:
            self.notify.error(e)

    # 弃用调的提交接口
    def on_result_submit1(self):
        try:
            if not check_type_model_instance.did_set:
                raise Exception('请选择标定类型！')
            self.notify.info("提交标定数据")

            for key, val in input_model_instance.inputs.items():
                self.glb_storage.update_inputs_data(key, val)
            result = result_model.results_all_ok(
                input_model_instance.get_input("maxTorque"),
                input_model_instance.get_input("minTorque"),
            )
            self.glb_storage.update_check_result_data(
                check_type_model_instance.is_first_check,
                result
            )

            selected_torque = ToolsModel().selected_torque
            # store\types.py 中dict函数ret.pop('toolTorqueInfo') 会将对象改变，需要先深度拷贝
            selected_orders = copy.deepcopy(OrdersModel().selected_orders)
            if selected_torque is None:
                raise Exception('无法提交：未选中工具')
            if selected_orders is None or len(selected_orders) == 0:
                raise Exception('无法提交：未选中工单')
            check = self.glb_storage.checkResult
            raw = True
            payload = publish_calibration_value_2_mom_wsdl(
                self._db_connect,
                selected_torque.toolFixedInspectionCode,
                selected_orders,
                selected_torque,
                check,
                raw
            )
            if not payload:
                raise Exception("未获取同步扭矩数据报文")
            self.notify.debug(f"发送标定数据payload: {pformat(payload, indent=4)}")
            if raw:
                full_url = self.glb_config.wsdl_base_url.split('?')[0]
                success, text = request_mom_data(full_url, data=payload)
            else:
                success, text = self._wsdl_client.do_request('TorqueCheckInfo', payload)
            if not success:
                raise Exception(text)
            self.notify.info(text)
            save_torque_check_status(
                selected_torque.toolFixedInspectionCode,
                selected_torque.torque,
                check_type_model_instance.is_first_check
            )
            self._order_controller.render()
            self._tools_controller.render_tools_pick_table()
        except Exception as e:
            self.notify.error(e)

    def init_sqlite_db(self):
        if self._db_connect:
            cr = self._db_connect.cursor()
            cr.execute('''
                CREATE TABLE IF NOT EXISTS ts013_wsdl(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                    orders TEXT
                )
            ''')
            cr.execute('''
                CREATE TABLE IF NOT EXISTS ts013_orders(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                    workcenter TEXT, 
                    schedule_date TIMESTAMP,
                    order_no TEXT NOT NULL UNIQUE , 
                    order_type TEXT, 
                    finished_product_no TEXT, 
                    first_checked INTEGER, 
                    rechecked INTEGER
                )
            ''')
            create_torque_check_status_table()
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
        ret = 0
        try:
            loop = QEventLoop()
            asyncio.set_event_loop(loop)
            # Show form
            self.window.showMaximized()
            # Run the program
            ret = self.app.exec()
        except Exception as e:
            self.notify.error(e)
            self._device_controller.device_disconnect()
        sys.exit(ret)

    def connect_signals(self):
        window = self.window
        ui = window.ui
        ### tab 1 曲线对比
        window.input_group.inputChanged.connect(self.on_input)
        ui.ToolsConfigAddButton.clicked.connect(self._tools_controller.add_tool)
        self._order_controller.selectedOrderChanged.connect(self._on_order_selected_change)
        self._check_type_radio.checkTypeChanged.connect(self.set_check_type)

    def set_check_type(self, is_first_check: bool):
        self.notify.debug('设置检测类型为：{}'.format('初检' if is_first_check else '复检'))
        check_type_model_instance.set_is_first_check(is_first_check)

    def _on_order_selected_change(self, orders: List[MOMOrder]):
        self._tools_controller.render_tools_pick_table()

    def on_input(self, key: str, value: Any):
        self.notify.debug('字段输入：{}，{}'.format(key, value))
        input_model_instance.update_inputs_data(key, value)
