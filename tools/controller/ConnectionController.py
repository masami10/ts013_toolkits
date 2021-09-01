from ..view import window as main_window
from store.config import Config

class ConnectionController:

    def __init__(self, window: main_window.ToolKitWindow, config: Config):
        self.window = window
        self.notify = self.window.notify_box
        self._config = config
        self.window.config_input_group.inputChanged.connect(self.on_config_input)
        self.window.person_config_group.inputChanged.connect(self.on_config_input1)
        self.render()
        self.render1()

    @property
    def contents(self):
        return {
            'orderUrl': self._config.get_config('orderUrl'),
            'momUrl': self._config.get_config('momUrl'),
            'operationUrl': self._config.get_config('operationUrl'),
            'workCenter': self._config.rawWorkCenters,
        }

    def on_config_input(self, key, value):
        if self.contents.get(key, None) == value:
            return
        self.notify.info('配置输入：{}，{}'.format(key, value))
        self._config.set_config(key, value)
        self.render()

    def render(self):
        self.window.config_input_group.set_texts(self.contents)


    @property
    def contents1(self):
        return {
            'originPersonCode': self._config.get_config('originPersonCode'),
            'originPersonName': self._config.get_config('originPersonName'),
            'recheckPersonCode': self._config.get_config('recheckPersonCode'),
            'recheckPersonName': self._config.get_config('recheckPersonName'),
        }

    def on_config_input1(self, key, value):
        if self.contents.get(key, None) == value:
            return
        self.notify.info('配置输入：{}，{}'.format(key, value))
        self._config.set_config(key, value)
        self.render1()

    def render1(self):
        self.window.person_config_group.set_texts(self.contents1)