from typing import List
from py_singleton import singleton
from store.types import MOMOrder
from store.sql import query_ts013_order_via_codes


@singleton
class OrdersModel:
    _orders: List[str]

    _selected_orders: List[MOMOrder]

    def __init__(self):
        self._orders = []
        self._selected_orders = []

    def set_orders(self, orders: List):
        order_no_list = [o.wipOrderNo for o in orders]
        self._orders = order_no_list

    @property
    def order_list(self) -> List[str]:
        return self._orders

    @property
    def selected_orders(self) -> List[MOMOrder]:
        return self._selected_orders

    @property
    def selected_order_codes(self) -> List[str]:
        return list(map(lambda o: o.wipOrderNo, self._selected_orders))

    def get_order_by_code(self, order_code) -> MOMOrder:
        return next(o for o in self._selected_orders if o.wipOrderNo == order_code)

    def toggle_select_order(self, order_code):
        if order_code in self.selected_orders:
            self._selected_orders.remove(order_code)
        else:
            orders = query_ts013_order_via_codes([order_code])  # 現在只能選擇一張訂單
            self._selected_orders = orders

    @property
    def selected_order_torques(self):
        torques = []
        for order in self._selected_orders:
            for k, v in order.toolTorqueInfo.items():
                torques.extend(v)
        return torques


orders_model_instance = OrdersModel()
