from zeep import Client, Settings
from loguru import logger
from zeep.cache import SqliteCache
from zeep.transports import Transport
import os
from distutils.util import strtobool
from requests import Response
from http import HTTPStatus
from lxml.etree import tostring
import sqlite3
from store.contants import TS013_DB_NAME

ENV_DEBUG_WSDL_REQ = strtobool(os.getenv('ENV_DEBUG_WSDL_REQ', 'false'))


class WSDLClient(object):
    _cache = SqliteCache(path='wsdl_cache.db', timeout=30)
    _settings = Settings(strict=False, xml_huge_tree=True, raw_response=True)

    def __init__(self, wsdl, wsdl_setting=_settings):
        self._wsdl = wsdl
        self._setting = wsdl_setting
        self._sqlite_conn = sqlite3.connect(TS013_DB_NAME)
        self._client = Client(self._wsdl, settings=self._setting, transport=Transport(cache=self._cache))

    def init_sqlite_db(self):
        if self._sqlite_conn:
            cr = self._sqlite_conn.cursor()
            cr.execute('''CREATE TABLE IF NOT EXISTS ts013_wsdl(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP
  DEFAULT CURRENT_TIMESTAMP, orders TEXT)''')
            cr.execute('''CREATE TABLE IF NOT EXISTS ts013_orders(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP
              DEFAULT CURRENT_TIMESTAMP, schedule_date TIMESTAMP,order_no TEXT, order_type TEXT, finished_product_no TEXT)''')
            self._sqlite_conn.commit()

    def __setattr__(self, key, value):
        if key == '_cache':  # cache不允许被赋值
            return
        super(WSDLClient, self).__setattr__(key, value)

    def do_request(self, method: str, data: dict) -> bool:
        m = self._client.service[method]
        if ENV_DEBUG_WSDL_REQ:
            node = self._client.create_message(self._client.service, method, **data)
            ss = tostring(node, encoding='utf-8', pretty_print=True)
            logger.info(f"发送WSDL数据: {ss}")
        if not m:
            logger.error(f"无法识别到方法： {method}, url: {self._wsdl}")
            return False
        resp: Response = m(**data)
        if resp.status_code >= HTTPStatus.BAD_REQUEST:
            logger.error(f"请求失败: {resp.content}")
            return False
        logger.debug(f"接收到原始数据：{resp.content}")
        return True
