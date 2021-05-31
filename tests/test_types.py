from unittest import TestCase
from store.types import ToolsInfo, checkInfoParams
from faker import Faker


class TestTypes(TestCase):

    def setUp(self) -> None:
        self._toolinfo = ToolsInfo('2132', '12313', '123123', '234234')
        self._checkinfoParams = checkInfoParams(self._toolinfo)

    def test_serialize_json(self):
        data = self._checkinfoParams.serialize_json()
        print(data)
