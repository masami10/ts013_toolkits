from unittest import TestCase
from transport.tcp_client import TcpClient
import time


class TestTcpClient(TestCase):

    def setUp(self) -> None:
        self.client = TcpClient(port=1222)

    def test_start(self):
        self.client.start()
        while True:
            time.sleep(1)
