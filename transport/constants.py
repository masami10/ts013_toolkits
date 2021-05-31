from store.contants import TS013_TZ, DEFAULT_DATETIME_FORMAT, request_body
import pytz
from copy import deepcopy
from datetime import datetime


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
