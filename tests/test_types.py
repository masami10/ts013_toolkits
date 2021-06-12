from unittest import TestCase
from store.types import ToolsInfo, checkInfoParams, MOMOrder
from requests_mock import Mocker
import json
from urllib.parse import urljoin
from store.store import StorageData


class TestTypes(TestCase):

    def setUp(self) -> None:
        self._toolinfo = ToolsInfo('2132', '12313', '123123', '234234')
        self._checkinfoParams = checkInfoParams(1, self._toolinfo)

    def test_serialize_json(self):
        data = self._checkinfoParams.serialize_json()
        print(data)


class TestMOMOrder(TestCase):
    def setUp(self) -> None:
        self._momorder = MOMOrder('003301554978', '231', 'M000002539447')
        self.store = StorageData()

    def test_do_generate_tool_torque_info(self):
        with Mocker() as mock_request:
            url = urljoin('http://localhost/test', self._momorder.partName)
            data = {
                "msg": {
                    "QCP00196": [
                        "[0.0]26012003833"
                    ],
                    "QCP00194": [
                        "[0.0]20M83826"
                    ],
                    "QCP00195": [
                        "[0.0]20M85015"
                    ],
                    "QCP00199": [
                        "[0.0]20M83670"
                    ]
                },
                "status_code": 200,
                "extra": ""
            }
            mock_request.get(url, text=json.dumps(data))
            self.store.do_generate_tool_torque_info(self._momorder)
