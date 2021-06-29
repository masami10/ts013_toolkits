from unittest import TestCase
from sqlite3 import Cursor, Connection, connect
from store.sql import insert_ts013_order_item, query_ts013_today_orders, query_ts013_order_via_fuzzy_code
from transport.constants import today, local_datetime_to_utc, local_date_from_str
from datetime import datetime
from store.contants import TS013_DB_NAME


class TestSQLTS013Order(TestCase):

    def setUp(self) -> None:
        self._db = connect(TS013_DB_NAME)
        cr = self._db.cursor()
        cr.execute('''CREATE TABLE IF NOT EXISTS ts013_orders(id INTEGER PRIMARY KEY AUTOINCREMENT, time TIMESTAMP
          DEFAULT CURRENT_TIMESTAMP, workcenter TEXT, schedule_date TIMESTAMP,order_no TEXT NOT NULL UNIQUE , order_type TEXT , finished_product_no TEXT)''')
        self._db.commit()

    def tearDown(self) -> None:
        self._db.close()

    def test_insert_ts013_order_item(self):
        cr = self._db
        rid = insert_ts013_order_item(cr, '111', '222', datetime.now(), 'no time zone')
        self._db.commit()
        self.assertIsInstance(rid, int)

    def test_insert_ts013_order_item_localtime_schedule_time(self):
        cr = self._db
        rid = insert_ts013_order_item(cr, '003301554976', '231', local_datetime_to_utc(local_date_from_str()),
                                      'M000002539446')
        self._db.commit()
        self.assertIsInstance(rid, int)

    def test_insert_ts013_order_item_localtime_schedule_time2(self):
        cr = self._db
        rid = insert_ts013_order_item(cr, '003301554977', '231', local_datetime_to_utc(local_date_from_str()),
                                      'M000002539446')
        self._db.commit()
        self.assertIsInstance(rid, int)

    def test_insert_ts013_order_item_localtime_schedule_time3(self):
        cr = self._db
        rid = insert_ts013_order_item(cr, '003301554978', '231', local_datetime_to_utc(local_date_from_str()),
                                      'M000002539447')
        self._db.commit()
        self.assertIsInstance(rid, int)

    def test_query_ts013_today_orders(self):
        cr = self._db
        ret = query_ts013_today_orders(cr)
        self.assertIsInstance(ret, list)

    def test_query_ts013_order_via_fuzzy_code(self):
        cr = self._db
        orders = query_ts013_order_via_fuzzy_code(cr, '00330155497')
        self.assertIsInstance(rid, list)
