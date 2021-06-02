from unittest import TestCase
import time
from transport.http_server import HttpServer, create_web_app
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import http
import json


class TestHttpDaemon(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        app = create_web_app()
        return app

    def setUp(self) -> None:
        super(TestHttpDaemon, self).setUp()
        self._server = HttpServer()

    @unittest_run_loop
    async def test_healthz_check_handler(self):
        resp = await self.client.request("GET", "/healthz")
        assert resp.status == http.HTTPStatus.NO_CONTENT

    @unittest_run_loop
    async def test_post_order_handler(self):
        with open('mock_order.json', encoding='utf-8') as f:
            body = json.load(f)

        resp = await self.client.request("POST", "/orders", json=body)
        assert resp.status == http.HTTPStatus.CREATED

    def test_run(self):
        self._server.run()
        while True:
            time.sleep(1)
