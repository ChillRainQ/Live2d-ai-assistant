from abc import ABC

from config.application_config import ApplicationConfig


class Live2dSetting:
    class CallbackSet(ABC):
        pass

    config: ApplicationConfig
    callbackSet: CallbackSet
    def __init__(self):
        super().__init__()

    def setup(self, config: ApplicationConfig, callbackSet: CallbackSet):
        self.config = config
        self.callbackSet = callbackSet