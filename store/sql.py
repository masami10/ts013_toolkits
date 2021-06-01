from sqlite3 import Cursor, Connection
from datetime import datetime
from transport.constants import today, tomorrow, local_date_from_str, local_datetime_to_utc
from typing import List, Any
from store.types import MOMOrder


def insert_ts013_tool_calibration_item(conn: Connection, identity: str) -> int:
    cr = conn.cursor()
    cr.execute("insert into ts013_wsdl (orders) values (?)", (identity), )
    ret = cr.lastrowid
    cr.close()
    return ret


def query_calibration_id_via_identity(conn: Connection, identity: str) -> int:
    cr = conn.cursor()
    cr.execute("SELECT id from ts013_wsdl where orders = ?", identity)
    result = cr.fetchone()
    cr.close()
    if not result:
        return 0
    return result[0]


def insert_ts013_order_item(conn: Connection, order_name: str, order_type: str, order_schedule_time: datetime,
                            finished_product: str) -> int:
    cr = conn.cursor()
    cr.execute("INSERT INTO  ts013_orders(order_no, order_type, finished_product_no, schedule_date) VALUES (?,?,?, ?)",
               (order_name, order_type, finished_product, order_schedule_time), )
    ret = cr.lastrowid
    cr.close()
    return ret


def query_ts013_today_orders(conn: Connection) -> List[MOMOrder]:
    prev = local_datetime_to_utc(local_date_from_str())
    nn = local_datetime_to_utc(tomorrow())
    results = query_ts013_order_via_schedule_date(conn, prev, nn)
    return results


def query_ts013_order_via_schedule_date(conn: Connection, prev: datetime, next: datetime) -> List[MOMOrder]:
    cr = conn.cursor()
    cr.execute("select * from ts013_orders where schedule_date between ? AND ?", (prev, next), )
    results = cr.fetchall()
    cr.close()
    ret = []
    for r in results:
        rid, create_at, schedule_time, order_no, order_type, finished_product_no = r
        m = MOMOrder(order_no, order_type, finished_product_no)
        ret.append(m)
    return ret
