from qfluentwidgets import ComboBoxSettingCard, FluentIcon

from config.application_config import ApplicationConfig
from ui.components.design.base_design import BaseDesign


class AiSettingDesign(BaseDesign):
    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        self.llm = ComboBoxSettingCard(config.llm_type, FluentIcon.CHAT, '对话模型', '选择对话使用的LLM', config.llm_list)
        self.tts = ComboBoxSettingCard(config.tts_type, FluentIcon.FEEDBACK, '语音合成', '选择语音合成使用的TTS', config.tts_list)
        self.vLayout.addWidget(self.llm)
        self.vLayout.addWidget(self.tts)
        self.vLayout.addStretch(1)
