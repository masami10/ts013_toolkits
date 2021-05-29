from tenacity import retry_if_result, retry_if_exception_type, wait_exponential, after_log, retry
from loguru import logger
import logging
import requests
import pprint
from http import HTTPStatus


def is_none_p(value):
    """Return True if value is None"""
    return value is None


retry(retry=(retry_if_result(is_none_p) | retry_if_exception_type()),
      wait=wait_exponential(multiplier=1, min=4, max=10),
      after=after_log(logger, logging.DEBUG))


def http_post_json_request(url, data=None):
    logger.debug('request data: {}'.format(pprint.pformat(data, indent=4)))
    if not data:
        return
    resp = requests.post(url, json=data)
    if resp.status_code >= HTTPStatus.BAD_REQUEST:
        logger.error(f'request Error: {resp.text}')
        return None
    return resp.json()
