import pandas as pd
from typing import List

from ..view import window as main_window
from PyQt5.QtWidgets import QCheckBox
from sqlite3 import Connection
from store.sql import query_ts013_today_orders
from store.store import StorageData


def select_tool_checkbox(order, on_select):
    t = QCheckBox()

    def on_button_clicked():
        on_select(order)

    t.clicked.connect(on_button_clicked)
    t.setText('')
    return t


class OrderController:
    _content: pd.DataFrame
    _selected_orders: List[str]

    def __init__(self, window: main_window.ToolKitWindow, db_connect: Connection, store: StorageData):
        self.window = window
        self._db_connect = db_connect
        self._store = store
        self.notify = self.window.notify_box
        self._content = pd.DataFrame({
            '订单号': [],
            '已选择': []
        })
        self._selected_orders = []
        ui = self.window.ui
        ui.load_order_btn.clicked.connect(self.load_orders)
        self.render()

    def load_orders(self):
        orders = query_ts013_today_orders(self._db_connect)
        order_no_list = [o.wipOrderNo for o in orders]
        self._content = pd.DataFrame({
            '订单号': order_no_list,
        })
        self.render()

    def render(self):
        orders = list(self._content['订单号'])

        content = pd.DataFrame({
            '订单号': orders,
            '选中': list(map(lambda o: select_tool_checkbox(o, self.on_order_clicked), orders))
        })
        self.window.order_table.render_table(content)

    def on_order_clicked(self, order_code: str):
        if order_code in self._selected_orders:
            self._selected_orders.remove(order_code)
        else:
            self._selected_orders.append(order_code)

        self._store.update_selected_orders(','.join(self._selected_orders))
        self.render_order_detail()

    def render_order_detail(self):
        orders_content = ', '.join(self._selected_orders)
        self.window.input_group.set_text('orderCode', orders_content)
