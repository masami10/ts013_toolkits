import pandas as pd
from typing import List
from PyQt5 import QtCore
from ..view import window as main_window
from ui.toolkit import Ui_MainWindow
from PyQt5.QtWidgets import QRadioButton
from sqlite3 import Connection
from store.sql import query_ts013_today_orders, query_ts013_order_via_fuzzy_code, \
    query_ts013_local_workcenter_today_orders, insert_ts013_order_item
from store.store import StorageData
from store.types import MOMOrder
from store.config import Config
from api.restful_api import request_get_last_one_week_orders
from http import HTTPStatus
from typing import Optional, Dict
from transport.constants import local_datetime_to_utc
from tools.model.OrdersModel import orders_model_instance as orders_model, OrdersModel
from PyQt5 import QtCore, QtWidgets


def select_tool_checkbox(order, on_select, selected: bool = False):
    t = QRadioButton()
    t.setChecked(selected)

    def on_button_clicked():
        on_select(order)

    t.clicked.connect(on_button_clicked)
    t.setText('')
    return t


class OrderController(QtCore.QObject):
    selectedOrderChanged = QtCore.pyqtSignal(list)

    def __init__(self, window: main_window.ToolKitWindow, db_connect: Connection, store: StorageData, config: Config):
        super(OrderController, self).__init__()
        self.window = window
        self._db_connect = db_connect
        self._store = store
        self._config = config
        self.notify = self.window.notify_box
        orders_model.set_orders([])
        ui: Ui_MainWindow = self.window.ui
        ui.load_order_btn.clicked.connect(self.load_today_orders)
        ui.load_server_order_btn.clicked.connect(self.load_last_one_week_orders)
        ui.filter_workcenter_btn.clicked.connect(self.load_local_today_orders)
        ui.QueryOrderButton.clicked.connect(self.query_orders_via_code)
        ui.CancelQueryButton.clicked.connect(self.load_all_orders)
        self.render()

    def query_orders_via_code(self):
        order_no = self.window.ui.QueryOrderCodeEdit.text()
        orders = query_ts013_order_via_fuzzy_code(self._db_connect, order_no)
        orders_model.set_orders(orders)
        self.render()

    def load_all_orders(self):
        orders = query_ts013_order_via_fuzzy_code(self._db_connect, '')
        orders_model.set_orders(orders)
        self.render()

    def load_local_today_orders(self):
        orders = query_ts013_local_workcenter_today_orders(self._db_connect)
        orders_model.set_orders(orders)
        self.render()

    def load_last_one_week_orders(self):
        try:
            workcenters = self._config.workCenters or []
            for workcenter in workcenters:
                success, resp = request_get_last_one_week_orders(self._config.get_order_url, workcenter)
                if not success:
                    msg = "request_get_last_one_week_orders 调用接口失败: {}".format(resp.text)
                    raise Exception(msg)
                data = resp.json()
                if data['status_code'] != HTTPStatus.OK:
                    msg = "request_get_last_one_week_orders 调用接口失败: {}".format(resp.text)
                    raise Exception(msg)
                orders: Optional[List] = data.get('msg', [])
                if not orders:
                    return
                o: Dict
                for o in orders:
                    order_schedule_time = o.get('order_schedule_time')
                    if order_schedule_time:
                        o.update({
                            'order_schedule_time': local_datetime_to_utc(order_schedule_time)
                        })
                    id = insert_ts013_order_item(self._db_connect, **o)
                    if id:
                        self.notify.info(f"订单: {o.get('order_name')}插入数据库成功")
                    else:
                        self.notify.info(f"订单: {o.get('order_name')}插入数据库失败")
        except Exception as e:
            raise e

    def load_today_orders(self):
        orders = query_ts013_today_orders(self._db_connect)
        orders_model.set_orders(orders)
        self.render()

    def render(self):
        orders = orders_model.order_list
        order_list_info: pd.DataFrame = orders_model.order_list_info
        content = pd.DataFrame({
            '订单号': orders,
            '标定状态': list(
                map(lambda info: OrdersModel.check_status(info.get('first_checked'), info.get('rechecked')),
                    order_list_info.to_dict('records')
                    )
            ),
            '选中': list(map(lambda o: select_tool_checkbox(o, self.on_order_clicked, o in orders_model.selected_orders),
                           orders))
        })
        table = self.window.order_table
        table.table_render_signal.emit(content)
        if not orders or len(orders) == 0:
            return
        header = table.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        for row in range(len(orders)):
            table.setRowHeight(row, 50)

    def on_order_clicked(self, order_code: str):
        orders_model.toggle_select_order(order_code)

        orders: List[MOMOrder] = self._store.update_selected_orders(','.join(orders_model.selected_orders))
        try:
            for o in orders:
                self._store.do_generate_tool_torque_info(self._config.get_tool_url, o)
            self.selectedOrderChanged.emit(orders)
            self.render_order_detail()
        except Exception as e:
            self.notify.error(e)

    def render_order_detail(self):
        orders_content = ', '.join(orders_model.selected_orders)
        self.window.input_group.set_text('orderCode', orders_content)
