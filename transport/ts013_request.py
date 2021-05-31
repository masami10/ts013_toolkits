# -*- coding: utf-8 -*-
import functools
import pprint
import json
import copy
from loguru import logger as _logger
import logging
from tenacity import retry, wait_random_exponential, RetryError, after_log
import requests
import os

ENV_RUNTIME_ENV = os.getenv('ENV_RUNTIME_ENV', 'test')

base_url = {
    'test': 'http://10.220.30.131:5000',
    'prod': 'http://10.220.30.158:7000'
}

TS013_BASE_URL = base_url.get(ENV_RUNTIME_ENV, base_url['test'])

DEFAULT_METHOD = 'post'

DEFAULT_HEADERS = {'Content-Type': 'application/json'}

API_LIST = {
    'base_info': (DEFAULT_METHOD, '/api/v1/base_data'),
    'product': (DEFAULT_METHOD, '/api/v1/product_data'),
    'dispatch': (DEFAULT_METHOD, '/api/v1/order_dispatching'),
    'doOrder': (DEFAULT_METHOD, '/api/v1/start_work'),
    'finishOrder': (DEFAULT_METHOD, '/api/v1/complete_work'),
    'fetchOrder': (DEFAULT_METHOD, '/api/v1/get_order')
}

AUTH_LIST = {
    'base_info': ('base_data', 'base_data'),
    'product': ('product_data', 'product_data'),
    'dispatch': ('order_dispatching', 'order_dispatching'),
    'doOrder': ('order_start', 'order_start'),
    'finishOrder': ('order_complete', 'order_complete'),
    'fetchOrder': ('get_order', 'get_order')
}


def _default_headers():
    return copy.deepcopy(DEFAULT_HEADERS)


def my_stop(retry_state):
    if isinstance(retry_state.outcome, ValueError) or retry_state.attempt_number >= 5:
        return True
    else:
        return False


@retry(stop=my_stop, wait=wait_random_exponential(multiplier=1, min=2, max=60), reraise=True,
       after=after_log(_logger, logging.INFO))
def _send_request(full_url, method, headers, data, auth=(), timeout=6):
    m = getattr(requests, method)
    if not m:
        raise ValueError('Can Not Found The Method: {}'.format(method))
    if data and method in ['post', 'put']:
        payload = json.dumps(data)
    else:
        payload = None
    if payload:
        return m(url=full_url, data=payload, headers=headers, timeout=timeout, auth=auth)
    else:
        return m(url=full_url, headers=headers, timeout=timeout, auth=auth)


def _do_ts013_request(url, method=DEFAULT_METHOD, data=None, headers=DEFAULT_HEADERS, auth=(), verify=False):
    try:
        _logger.debug('Do Request: {}, Data: {}'.format(url, pprint.pformat(data, indent=4)))
        resp = _send_request(full_url=url, method=method, data=data, headers=headers, auth=auth)
        if resp.status_code > 400:
            raise Exception(
                'Do Request: {} Fail, Status Code: {}, resp: {}'.format(url, resp.status_code, resp.text))
        else:
            return resp.json()
    except Exception as e:
        _logger.exception(f'TS013 Request URL:{url} Except: {e}')
        raise e


def ts013_request(entity):
    def decorator(f):
        @functools.wraps(f)
        def request_wrap(*args, **kw):
            data = f(*args, **kw)
            if data and not isinstance(data, dict):
                _logger.error('Function: {0}.{1}, TS013 Request Data Is Invalid'.format(f.__module__, f.__name__))
                return None
            if entity not in AUTH_LIST:
                raise Exception('Can Not Get AUTH')
            auth = AUTH_LIST[entity]
            headers = _default_headers()
            method, full_url = ts013_get_method_full_url(entity=entity)
            return _do_ts013_request(full_url, method, data, headers, auth, verify=False)

        return request_wrap

    return decorator


def ts013_get_method_full_url(entity):
    if entity not in API_LIST.keys():
        raise Exception('Can Not Get Endpoint')
    method, endpoint = API_LIST.get(entity)
    full_path = '{}{}'.format(TS013_BASE_URL, endpoint)
    return method, full_path
