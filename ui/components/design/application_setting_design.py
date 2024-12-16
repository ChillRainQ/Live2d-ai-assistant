from config.application_config import ApplicationConfig
from ui.components.cards import RangeItemSettingCard
from ui.components.design.base_design import BaseDesign


class ApplicationSettingDesign(BaseDesign):

    def __init__(self, config: ApplicationConfig):
        super().__init__()
        self.resource_dir = config.resource_dir.value

        self.fps = RangeItemSettingCard(config.fps, "", "FPS")
        self.scale = RangeItemSettingCard(config.scale, "", "缩放比例")
        self.canvas_width = RangeItemSettingCard(config.width, "", "画布宽度")
        self.canvas_height = RangeItemSettingCard(config.height, "", "画布高度")
        self.lip_sync = RangeItemSettingCard(config.lip_sync, "", "嘴型同步比率")



        self.vLayout.addWidget(self.fps)
        self.vLayout.addWidget(self.canvas_width)
        self.vLayout.addWidget(self.canvas_height)
        self.vLayout.addWidget(self.scale)
        self.vLayout.addWidget(self.lip_sync)