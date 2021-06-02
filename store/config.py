from config import settings
from dynaconf import Dynaconf
from dynaconf import loaders
from dynaconf.utils.boxing import DynaBox
import os
import pathlib
from py_singleton import singleton

ENV_RUNTIME_ENV = os.getenv('ENV_RUNTIME_ENV', 'test')


@singleton
class Config(object):
    def __init__(self):
        self._settings: Dynaconf = settings
        self._filename = pathlib.WindowsPath(os.getcwd()).joinpath('settings.toml')

    def load_test_config(self):
        self._settings.key = "value"
        self._settings.dd = '123123'

    def save_config(self):
        data = self._settings.as_dict()
        loaders.write(str(self._filename), DynaBox(data).to_dict())

    def set_config(self, key, value):
        setattr(self._settings, key, value)
        self.save_config()

    def set_tools_config(self, value: dict):
        setattr(self._settings, 'tools', value)
        self.save_config()

    def del_tool_config(self, tool_inspect_code: str):
        tool_config = self.tools_config
        v = list(filter(lambda c: c.toolFixedInspectionCode != tool_inspect_code, tool_config))
        self.set_tools_config(v)

    @property
    def tools_config(self):
        return getattr(self._settings, 'tools')

    def get_config(self, key):
        try:
            return getattr(self._settings, key)
        except Exception as e:
            return None
