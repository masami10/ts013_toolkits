from ..view import window as main_window
from store.config import Config

class ConnectionController:

    def __init__(self, window: main_window.ToolKitWindow, config: Config):
        self.window = window
        self.notify = self.window.notify_box
        self._config = config
        self.window.config_input_group.inputChanged.connect(self.on_config_input)
        self.render()

    @property
    def contents(self):
        return {
            'orderUrl': self._config.get_config('orderUrl'),
            'momUrl': self._config.get_config('momUrl'),
        }

    def on_config_input(self, key, value):
        if self.contents.get(key, None) == value:
            return
        self.notify.info('配置输入：{}，{}'.format(key, value))
        self._config.set_config(key, value)
        self.render()

    def render(self):
        self.window.config_input_group.set_texts(self.contents)
