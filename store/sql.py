from sqlite3 import Cursor, Connection, IntegrityError, Row
from datetime import datetime
from transport.constants import tomorrow, local_date_from_str, local_datetime_to_utc, months
from typing import List
from store.types import MOMOrder
from store.config import Config
from loguru import logger
from store.contants import TS013_DB_NAME
import sqlite3
import pandas as pd

glb_config = Config()

DEFAULT_CONNECTION = sqlite3.connect(TS013_DB_NAME)


def with_connection(func):
    def dec(*args, conn: Connection = None, **kwargs):
        if not conn:
            conn = DEFAULT_CONNECTION
        return func(*args, conn=conn, **kwargs)

    return dec


def insert_ts013_tool_calibration_item(conn: Connection, identity: str) -> int:
    cr = conn.cursor()
    cr.execute("insert into ts013_wsdl (orders) values (?)", (identity,), )
    ret = cr.lastrowid
    cr.close()
    return ret


def query_calibration_id_via_identity(conn: Connection, identity: str) -> int:
    cr = conn.cursor()
    cr.execute("SELECT id from ts013_wsdl where orders = ?", (identity,), )
    result = cr.fetchone()
    cr.close()
    if not result:
        return 0
    return result[0]


def insert_ts013_order_item(conn: Connection, order_name: str, order_type: str, order_schedule_time: datetime,
                            finished_product: str, workcenter: str = glb_config.workCenters[0]) -> int:
    cr = conn.cursor()
    try:
        cr.execute(
            "INSERT INTO  ts013_orders(order_no, order_type, finished_product_no, schedule_date, workcenter) VALUES (?,?,?, ?, ?)",
            (order_name, order_type, finished_product, order_schedule_time, workcenter), )
        ret = cr.lastrowid
        conn.commit()
    except IntegrityError as e:
        logger.error(f'insert_ts013_order_item错误: {e}')
        return 0
    finally:
        cr.close()
    return ret


def query_ts013_today_orders(conn: Connection) -> List[MOMOrder]:
    prev = local_datetime_to_utc(local_date_from_str())
    nn = local_datetime_to_utc(tomorrow())
    results = query_ts013_order_via_schedule_date(conn, prev, nn)
    return results


def query_ts013_local_workcenter_today_orders(conn: Connection) -> List[MOMOrder]:
    prev = local_datetime_to_utc(local_date_from_str())
    workcenters = glb_config.workCenters
    nn = local_datetime_to_utc(tomorrow())
    results = query_ts013_order_via_schedule_date(conn, prev, nn)
    rs = list(filter(lambda s: s.workCenter in workcenters, results))
    return rs


def row_keys_to_idxs(keys, key_list):
    idxs = []
    for key in keys:
        if key not in key_list:
            raise Exception('尝试获取错误的key: {}'.format(key))
        idx = key_list.index(key)
        idxs.append(idx)
    return idxs


def ts013_model_2_order_obj(cr: Cursor) -> List[MOMOrder]:
    ks = list(map(lambda d: d[0], cr.description))
    idxs = row_keys_to_idxs(['order_no', 'order_type', 'finished_product_no', 'workcenter'], ks)
    results = cr.fetchall()
    ret = []
    for r in results:
        m = MOMOrder(*list(map(lambda i: r[i], idxs)))
        ret.append(m)
    return ret


def query_ts013_order_via_fuzzy_code(conn: Connection, order_no: str = '') -> List[MOMOrder]:
    cr = conn.cursor()
    if not order_no:
        prev = local_datetime_to_utc(months(3, prev=True))
        nn = local_datetime_to_utc(tomorrow())
        ret = query_ts013_order_via_schedule_date(conn, prev, nn)
    else:
        query = f'''SELECT * FROM ts013_orders WHERE order_no LIKE '%{order_no}%' '''
        cr.execute(query)
        ret = ts013_model_2_order_obj(cr)
        cr.close()
    return ret


def query_ts013_order_via_codes(conn: Connection, orders: List[str]) -> List[MOMOrder]:
    cr = conn.cursor()
    query = f"SELECT * FROM ts013_orders WHERE order_no in ({','.join(['?'] * len(orders))})"
    cr.execute(query, orders)
    ret = ts013_model_2_order_obj(cr)
    cr.close()
    return ret


def query_ts013_order_via_schedule_date(conn: Connection, prev: datetime, next: datetime) -> List[MOMOrder]:
    cr = conn.cursor()
    cr.execute("select * from ts013_orders where schedule_date between ? AND ?", (prev, next), )
    ret = ts013_model_2_order_obj(cr)
    cr.close()
    return ret


def result_to_dataframe(cr: Cursor) -> pd.DataFrame:
    cols = list(map(lambda d: d[0], cr.description))
    data = []
    for row in cr.fetchall():
        data.append([*row])
    return pd.DataFrame(data=data, columns=cols)


@with_connection
def query_order_list_info(order_nos, conn: Connection = None) -> pd.DataFrame:
    cr = conn.cursor()
    cr.execute(f'''
        SELECT order_no, first_checked, rechecked FROM ts013_orders where order_no in ({','.join(['?'] * len(order_nos))})
    ''', order_nos)
    df = result_to_dataframe(cr)
    cr.close()
    return df


@with_connection
def set_order_check_status(order_nos, conn: Connection = None, is_first_check=True, status=True):
    status_int = 1 if status else 0
    cr = conn.cursor()
    if is_first_check:
        query = f'''
        UPDATE ts013_orders 
        SET first_checked = ? 
        WHERE order_no in ({','.join(['?'] * len(order_nos))});
        '''
        cr.execute(query, (status_int, *order_nos), )
    else:
        cr.execute(f'''
            UPDATE ts013_orders 
            SET rechecked = ? 
            WHERE order_no in ({','.join(['?'] * len(order_nos))});
        ''', (status_int, *order_nos), )
    cr.close()
    conn.commit()
