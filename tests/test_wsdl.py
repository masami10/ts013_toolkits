from unittest import TestCase
from api.wsdl import MOMOrder, serialize_mom_orders
import json


class TestWSDLAPI(TestCase):

    def setUp(self) -> None:
        self._momOrders = list()
        self._momOrders.append(MOMOrder('111', '1', '15'))
        self._momOrders.append(MOMOrder('112', '1', '16'))
        self._momOrders.append(MOMOrder('113', '1', '17'))

    def test_serialize_mom_orders(self):
        data = serialize_mom_orders(self._momOrders)
