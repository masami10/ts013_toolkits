from unittest import TestCase
import time
from transport.http_server import HttpDaemon, create_web_app
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import http


class TestHttpDaemon(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        app = create_web_app()
        return app

    def setUp(self) -> None:
        super(TestHttpDaemon, self).setUp()
        self._server = HttpDaemon()

    @unittest_run_loop
    async def test_healthz_check_handler(self):
        resp = await self.client.request("GET", "/healthz")
        assert resp.status == http.HTTPStatus.NO_CONTENT

    def test_run(self):
        self._server.run()
        while True:
            time.sleep(1)
