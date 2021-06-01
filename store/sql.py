from sqlite3 import Cursor
from datetime import datetime
from transport.constants import today, tomorrow, local_date_from_str, local_datetime_to_utc


def insert_ts013_tool_calibration_item(cr: Cursor, identity: str) -> int:
    cr.execute("insert into ts013_wsdl (orders) values (?)", (identity), )
    return cr.lastrowid


def query_calibration_id_via_identity(cr: Cursor, identity: str) -> int:
    cr.execute("SELECT id from ts013_wsdl where orders = ?", identity)
    result = cr.fetchone()
    if not result:
        return 0
    return result[0]


def insert_ts013_order_item(cr: Cursor, order_name: str, order_type: str, order_schedule_time: datetime,
                            finished_product: str) -> int:
    cr.execute("INSERT INTO  ts013_orders(order_no, order_type, finished_product_no, schedule_date) VALUES (?,?,?, ?)",
               (order_name, order_type, finished_product, order_schedule_time), )
    return cr.lastrowid


def query_ts013_today_orders(cr: Cursor):
    prev = local_datetime_to_utc(local_date_from_str())
    nn = local_datetime_to_utc(tomorrow())
    results = query_ts013_order_via_schedule_date(cr, prev, nn)
    return results


def query_ts013_order_via_schedule_date(cr: Cursor, prev: datetime, next: datetime) -> int:
    cr.execute("select * from ts013_orders where schedule_date between ? AND ?", (prev, next), )
    results = cr.fetchall()
    return results

