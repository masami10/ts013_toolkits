from transport.ts013_request import ts013_request
from transport.constants import create_new_request_body
from tenacity import retry, wait_random_exponential, RetryError, after_log
import requests
from loguru import logger as _logger
import logging
from transport.ts013_request import my_stop
from http import HTTPStatus


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


@retry(stop=my_stop, wait=wait_random_exponential(multiplier=1, min=2, max=60), reraise=True,
       after=after_log(_logger, logging.INFO))
def request_mom_data(full_url, data: str) -> (bool, str):
    headers = {'Content-Type': 'application/soap+xml; charset=utf-8'}
    if not data:
        _logger.error("数据为空")
        return
    resp = requests.post(url=full_url, data=data, headers=headers, timeout=5)
    if resp.status_code != HTTPStatus.OK:
        _logger.error("Error")
        return False, "调用接口失败: {}".format(resp.text)
    else:
        return True, "调用接口成功: {}".format(resp.text)
