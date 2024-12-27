from config.application_config import ApplicationConfig
from core.gobal_components import i18n
from ui.components.cards import RangeItemSettingCard
from ui.components.design.base_design import BaseDesign


class ApplicationSettingDesign(BaseDesign):

    def __init__(self, config: ApplicationConfig):
        super().__init__()
        self.resource_dir = config.resource_dir.value
        # ui.components.design.application_setting_design.setting.fps
        self.fps = RangeItemSettingCard(config.fps, "", f'{i18n.get_str("ui.components.design.application_setting_design.setting.fps")}')
        # ui.components.design.application_setting_design.setting.scale
        self.scale = RangeItemSettingCard(config.scale, "", f'{i18n.get_str("ui.components.design.application_setting_design.setting.scale")}')
        # ui.components.design.application_setting_design.setting.canvas_width
        self.canvas_width = RangeItemSettingCard(config.width, "", f'{i18n.get_str("ui.components.design.application_setting_design.setting.canvas_width")}')
        # ui.components.design.application_setting_design.setting.canvas_height
        self.canvas_height = RangeItemSettingCard(config.height, "", f'{i18n.get_str("ui.components.design.application_setting_design.setting.canvas_height")}')
        # ui.components.design.application_setting_design.setting.lip_sync
        self.lip_sync = RangeItemSettingCard(config.lip_sync, "", f'{i18n.get_str("ui.components.design.application_setting_design.setting.lip_sync")}')



        self.vLayout.addWidget(self.fps)
        self.vLayout.addWidget(self.canvas_width)
        self.vLayout.addWidget(self.canvas_height)
        self.vLayout.addWidget(self.scale)
        self.vLayout.addWidget(self.lip_sync)