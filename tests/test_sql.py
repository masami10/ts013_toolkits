from unittest import TestCase
from sqlite3 import Cursor, Connection, connect
from store.sql import insert_ts013_order_item, query_ts013_today_orders
from transport.constants import today, local_datetime_to_utc, local_date_from_str
from datetime import datetime


class Test(TestCase):

    def setUp(self) -> None:
        self._db = connect('./test.db')
        cr = self._db.cursor()
        cr.execute('''CREATE TABLE IF NOT EXISTS ts013_orders(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP
          DEFAULT CURRENT_TIMESTAMP, schedule_date TIMESTAMP,order_no TEXT, order_type TEXT, finished_product_no TEXT)''')
        self._db.commit()

    def tearDown(self) -> None:
        self._db.close()

    def test_insert_ts013_order_item(self):
        cr = self._db.cursor()
        rid = insert_ts013_order_item(cr, '111', '222', datetime.now(), '6666')
        self._db.commit()
        self.assertIsInstance(rid, int)

    def test_insert_ts013_order_item_localtime_schedule_time(self):
        cr = self._db.cursor()
        rid = insert_ts013_order_item(cr, '111', '222', local_datetime_to_utc(local_date_from_str()), '6666')
        self._db.commit()
        self.assertIsInstance(rid, int)

    def test_query_ts013_today_orders(self):
        cr = self._db.cursor()
        ret = query_ts013_today_orders(cr)
        print(ret)