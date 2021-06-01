from unittest import TestCase
from transport.constants import local_date_from_str, local_datetime_to_utc
from datetime import datetime


class Test(TestCase):
    def test_date_from_str(self):
        ss = "2021-05-21"
        d = local_date_from_str(ss)
        self.assertIsInstance(d, datetime)
        dd = local_datetime_to_utc(d)
        self.assertIsInstance(dd, datetime)
