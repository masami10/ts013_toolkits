from unittest import TestCase
from store.config import Config
from config import settings


class TestConfig(TestCase):

    def setUp(self) -> None:
        self._config = Config()

    def test_save_config(self):
        self._config.load_test_config()
        self._config.save_config()

    def test_config_assert(self):
        self.assertEqual(self._config._settings.key, "value")