import pandas as pd
from typing import List

from ..view import window as main_window
from PyQt5.QtWidgets import QCheckBox
from sqlite3 import Connection
from store.sql import query_ts013_today_orders


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

    def __init__(self, window: main_window.ToolKitWindow, db_connect: Connection):
        self.window = window
        self._db_connect = db_connect
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
        # todo: 修改渲染内容
        orders = list(self._content['订单号'])

        content = pd.DataFrame({
            '订单号': orders,
            '选中': list(map(lambda o: select_tool_checkbox(o, self.on_order_clicked), orders))
        })
        self.window.order_table.render(content)

    def on_order_clicked(self, order):
        if order in self._selected_orders:
            self._selected_orders.remove(order)
        else:
            self._selected_orders.append(order)
        self.render_order_detail()

    def render_order_detail(self):
        orders_content = ', '.join(self._selected_orders)
        self.window.input_group.set_text('orderCode', orders_content)
