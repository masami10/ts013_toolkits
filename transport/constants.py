# -*- coding: utf-8 -*-

from datetime import datetime
import pytz
import os
from copy import deepcopy

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


def now():
    today_utc = datetime.now()
    if isinstance(today_utc, str):
        today_utc = datetime.now().replace(microsecond=0, tzinfo=pytz.utc)
    return today_utc.astimezone(TS013_TZ).strftime(DEFAULT_DATETIME_FORMAT)


def create_new_request_body(system_type=None):
    today_utc = datetime.now()
    if isinstance(today_utc, str):
        today_utc = datetime.now().replace(microsecond=0, tzinfo=pytz.utc)
    r = deepcopy(request_body)
    r['esbInfo'].update({
        'requestTime': today_utc.astimezone(TS013_TZ).strftime(DEFAULT_DATETIME_FORMAT)
    })
    r['requestInfo'].update({
        'UpdateDate': today_utc.astimezone(TS013_TZ).strftime(DEFAULT_DATETIME_FORMAT)
    })
    if system_type:
        r['requestInfo'].update({
            'SystemType': system_type
        })
    return r
