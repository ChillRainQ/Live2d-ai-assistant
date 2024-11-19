from config.application_config import ApplicationConfig
from ui.components.design.base_design import BaseDesign


class ApplicationSettingDesign(BaseDesign):

    def __init__(self, config: ApplicationConfig):
        super().__init__()
        self.resource_dir = config.resource_dir.value
        # self.lip_sync