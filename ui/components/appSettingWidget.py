from config.application_config import ApplicationConfig
from ui.components.design.base_design import BaseDesign


class AppSettingWidget(BaseDesign):
    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        self.setObjectName('app_setting')
