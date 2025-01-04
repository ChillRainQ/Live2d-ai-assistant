from config.application_config import ApplicationConfig
from ui.components.design.application_setting_design import ApplicationSettingDesign


class SceneShowSetting(ApplicationSettingDesign):

    config: ApplicationConfig

    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        self.config = config
        self.setObjectName("scene_show_setting")
