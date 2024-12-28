from config.application_config import ApplicationConfig
from ui.components.design.ai_setting_design import AiSettingDesign


class AiSetting(AiSettingDesign):
    config: ApplicationConfig

    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        self.config = config
        self.setObjectName("ai_setting")