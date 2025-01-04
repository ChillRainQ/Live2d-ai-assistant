import abc
from abc import ABC

from config.application_config import ApplicationConfig
from ui.components.design.ai_setting_design import AiSettingDesign


class AiSetting(AiSettingDesign):
    class CallBackSet(ABC):
        @abc.abstractmethod
        def flash_llm(self):
            pass

        @abc.abstractmethod
        def flash_tts(self):
            pass
    config: ApplicationConfig
    callback: CallBackSet

    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        self.config = config
        self.setObjectName("ai_setting")

    def slotConnectSignal(self):
        self.config.llm_type.valueChanged.connect(self.callback.flash_llm)
        self.config.tts_type.valueChanged.connect(self.callback.flash_tts)

    def setup(self, callback: CallBackSet):
        self.callback = callback
        self.slotConnectSignal()
