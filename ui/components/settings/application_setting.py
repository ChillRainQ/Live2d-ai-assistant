from config.application_config import ApplicationConfig
from ui.components.design.application_setting_design import ApplicationSettingDesign


class ApplicationSetting(ApplicationSettingDesign):
    config: ApplicationConfig
    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        self.config = config
        self.setObjectName("application_setting")

    def setup(self):
        pass