from qfluentwidgets import FluentWindow

from config.application_config import ApplicationConfig
from ui.components.settings.live2d_setting import Live2dSetting


class Settings(FluentWindow):
    live2d_setting: Live2dSetting
    # llm_setting: LLMSetting
    # tts_setting: TTSSetting
    # asr_setting: ASRSetting
    # application_setting: ApplicationSetting
    config: ApplicationConfig

    def __init__(self, config: ApplicationConfig):
        pass

    def setup(self):
        pass

    def show(self):
        pass