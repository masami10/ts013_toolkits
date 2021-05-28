from typing import Any


class ToolKitMixin(object):

    def __init__(self, instance: Any, *args, **kwargs):
        self._qt_instance = instance

    @property
    def qt_instance(self):
        return self._qt_instance

    def __getattr__(self, item):
        if self.qt_instance:
            return getattr(self._qt_instance, item)
