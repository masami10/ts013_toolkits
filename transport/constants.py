from store.contants import TS013_TZ, DEFAULT_DATETIME_FORMAT, request_body, DEFAULT_DATE_FORMAT
import pytz
from copy import deepcopy
from typing import Union
from datetime import datetime, date, timedelta

DATE_LENGTH = len(date.today().strftime(DEFAULT_DATE_FORMAT))


def local_datetime_from_str(ss: str = '') -> datetime:
    ll = len(ss)
    if ll < DATE_LENGTH:
        d = datetime.now()
    elif len(ss) == DATE_LENGTH:
        d = datetime.strptime(ss, DEFAULT_DATE_FORMAT)
    else:
        d = datetime.strptime(ss, DEFAULT_DATETIME_FORMAT)
    return TS013_TZ.localize(d)


def local_datetime_to_utc(dd: Union[datetime, str]) -> datetime:
    if isinstance(dd, str):
        dd = local_datetime_from_str(dd)
    return TS013_TZ.normalize(dd).astimezone(pytz.utc)


def local_date_from_str(ss: str = '') -> datetime:
    if len(ss) < DATE_LENGTH:
        d = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        d = datetime.strptime(ss, DEFAULT_DATE_FORMAT)
    return TS013_TZ.localize(d)


def now() -> str:
    now_utc = datetime.now()
    if isinstance(now_utc, str):
        now_utc = datetime.now().replace(microsecond=0, tzinfo=pytz.utc)
    return now_utc.astimezone(TS013_TZ).strftime(DEFAULT_DATETIME_FORMAT)


def tomorrow() -> str:
    tomorrow_utc = datetime.today() + timedelta(days=1)
    return tomorrow_utc.astimezone(TS013_TZ).strftime(DEFAULT_DATE_FORMAT)


def months(d, prev=False) -> str:
    delta = int(d * 4)
    if prev:
        tomorrow_utc = datetime.today() - timedelta(weeks=delta)
    else:
        tomorrow_utc = datetime.today() + timedelta(weeks=delta)
    return tomorrow_utc.astimezone(TS013_TZ).strftime(DEFAULT_DATE_FORMAT)


def today() -> str:
    today_utc = datetime.today()
    if isinstance(today_utc, str):
        today_utc = datetime.today().replace(tzinfo=pytz.utc)
    return today_utc.astimezone(TS013_TZ).strftime(DEFAULT_DATE_FORMAT)


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
