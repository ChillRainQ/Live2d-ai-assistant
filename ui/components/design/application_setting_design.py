from qfluentwidgets import FluentIcon

from config.application_config import ApplicationConfig
from core.gobal_components import i18n
from ui.components.cards import RangeItemSettingCard, SelectSettingCard, RangeDoubleItemSettingCard
from ui.components.design.base_design import BaseDesign


class ApplicationSettingDesign(BaseDesign):

    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        # self.resource_dir = config.resource_dir.value
        # ui.components.design.application_setting_design.setting.fps
        self.fps = RangeItemSettingCard(config.fps, FluentIcon.VIEW, f'{i18n.get_str("ui.components.design.application_setting_design.setting.fps")}','每秒钟刷新次数（并非越高越好，推荐50-60）')
        # ui.components.design.application_setting_design.setting.canvas_width
        self.canvas_width = RangeItemSettingCard(config.width, FluentIcon.SCROLL, f'{i18n.get_str("ui.components.design.application_setting_design.setting.canvas_width")}', '画布的长度')
        # ui.components.design.application_setting_design.setting.canvas_height
        self.canvas_height = RangeItemSettingCard(config.height, FluentIcon.SCROLL, f'{i18n.get_str("ui.components.design.application_setting_design.setting.canvas_height")}', '画布的宽度')
        # ui.components.design.application_setting_design.setting.lip_sync
        self.lip_sync = RangeItemSettingCard(config.lip_sync, FluentIcon.SYNC, f'{i18n.get_str("ui.components.design.application_setting_design.setting.lip_sync")}','语音的嘴型同步率，数字越大动作越大')
        # ui.components.design.application_setting_design.setting.scale
        # self.scale = RangeItemSettingCard(config.scale, FluentIcon.FULL_SCREEN, f'{i18n.get_str("ui.components.design.application_setting_design.setting.scale")}','相对于画布的缩放比率')
        self.scale = RangeDoubleItemSettingCard(config.scale, FluentIcon.FULL_SCREEN, f'{i18n.get_str("ui.components.design.application_setting_design.setting.scale")}','相对于画布的缩放比率')
        # ui.components.design.application_setting_design.setting.language
        self.language = SelectSettingCard(config.language, config.language_list, FluentIcon.LANGUAGE, f'{i18n.get_str("ui.components.design.application_setting_design.setting.language")}', '实验中的多语言支持')



        self.vLayout.addWidget(self.fps)
        self.vLayout.addWidget(self.canvas_width)
        self.vLayout.addWidget(self.canvas_height)
        self.vLayout.addWidget(self.scale)
        self.vLayout.addWidget(self.lip_sync)
        self.vLayout.addWidget(self.language)
        self.vLayout.addStretch(1)