import pandas as pd
from typing import List
from store.sql import query_order_list_info


class OrdersModel:
    _orders: List

    _selected_orders: List

    def __init__(self):
        self._orders = []
        self._selected_orders = []

    def set_orders(self, orders: List):
        order_no_list = [o.wipOrderNo for o in orders]
        self._orders = order_no_list

    @property
    def order_list(self):
        return self._orders

    @property
    def selected_orders(self):
        return self._selected_orders

    def toggle_select_order(self, order_code):
        if order_code in self.selected_orders:
            self._selected_orders.remove(order_code)
        else:
            self._selected_orders = [order_code]  # 現在只能選擇一張訂單

    @property
    def order_list_info(self) -> pd.DataFrame:
        return query_order_list_info(self._orders)

    @staticmethod
    def check_status(first_check_status, recheck_status):
        if recheck_status == 1:
            return '已复检'
        if first_check_status == 1:
            return '已初检'
        return '未标定'


orders_model_instance = OrdersModel()
