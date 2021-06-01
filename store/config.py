from config import settings
from dynaconf import Dynaconf
from dynaconf import loaders
from dynaconf.utils.boxing import DynaBox
import os
import pathlib

ENV_RUNTIME_ENV = os.getenv('ENV_RUNTIME_ENV', 'test')


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
