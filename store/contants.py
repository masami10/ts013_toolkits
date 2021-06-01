# -*- coding: utf-8 -*-

import pytz
import os

TS013_TZ = pytz.timezone('Asia/Shanghai')

ENV_SYSTEM_TYPE = os.getenv('ENV_SYSTEM_TYPE', '101')

request_body = {
    "esbInfo": {
        "instId": "",
        "requestTime": "",
        "attr1": "",
        "attr2": "",
        "attr3": ""
    },
    "requestInfo": {
        "SystemType": ENV_SYSTEM_TYPE,
        "UpdateDate": "2021-03-15",
    }
}

DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DEFAULT_DATE_FORMAT = '%Y-%m-%d'


TS013_DB_NAME = 'x_conn.db'


