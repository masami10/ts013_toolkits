from transport.ts013_request import ts013_request
from transport.constants import create_new_request_body


@ts013_request('fetchOrder')
def fetch_workorder_request(ordernumber, orderType, operationCode, system_type=None):
    # todo: 字段不明确
    data = create_new_request_body(system_type)
    data['requestInfo'].update(
        {
            "WIPORDERNO": ordernumber,
            "WIPORDERTYPE": orderType,
            "OPRSEQUENCENO": operationCode,
            "DUMMY1": "",
            "DUMMY2": "",
            "DUMMY3": ""
        })
    return data
