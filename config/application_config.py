import os

from qfluentwidgets import ConfigItem, QConfig, RangeConfigItem, RangeValidator, BoolValidator, OptionsConfigItem, \
    OptionsValidator

from core.gobal_components import i18n

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME = "config.json"
CONFIG_FILE = os.path.join(CURRENT_DIR, CONFIG_FILE_NAME)
class ApplicationConfig(QConfig):
    live2d_name: ConfigItem = ConfigItem("live2d", "name", "nn")
    resource_dir: ConfigItem = ConfigItem("live2d", "resource_dir", "resources/v3")
    scale: RangeConfigItem = RangeConfigItem("live2d", "scale", 1.0, RangeValidator(0, 1))
    drawX: RangeConfigItem = RangeConfigItem("live2d", "drawX", 0.0, RangeValidator(-2.0, 2.0))
    drawY: RangeConfigItem = RangeConfigItem("live2d", "drawY", 0.0, RangeValidator(-2.0, 2.0))
    autoBlink: ConfigItem = ConfigItem("live2d", "autoBlink", True, BoolValidator())
    autoBreath: ConfigItem = ConfigItem("live2d", "autoBreath", True, BoolValidator())

    fps: RangeConfigItem = RangeConfigItem("scene", "fps", 60, RangeValidator(1, 120))
    width: RangeConfigItem = RangeConfigItem("scene", "width", 400, RangeValidator(1, 10000))
    height: RangeConfigItem = RangeConfigItem("scene", "height", 600, RangeValidator(1, 10000))
    lastX: RangeConfigItem = RangeConfigItem("scene", "lastX", 0, RangeValidator(0, 10000))
    lastY: RangeConfigItem = RangeConfigItem("scene", "lastY", 0, RangeValidator(0, 10000))
    stay_on_top: ConfigItem = ConfigItem("scene", "stay_on_top", True, BoolValidator())
    visible: ConfigItem = ConfigItem("scene", "visible", True, BoolValidator())
    motion_interval: RangeConfigItem = RangeConfigItem("scene", "motion_interval", 10, RangeValidator(5, 86400))
    clickPenetrate: ConfigItem = ConfigItem("scene", "clickPenetrate", False, BoolValidator())
    eye_track: ConfigItem = ConfigItem("scene", "eye_track", True, BoolValidator())
    lip_sync: RangeConfigItem = RangeConfigItem("scene", "lip_sync", 2.0, RangeValidator(0, 10))

    icon: ConfigItem = ConfigItem("tray", "icon", "resources/icon.png")

    asr: ConfigItem = ConfigItem("asr", "asr", False, BoolValidator())
    asr_type: ConfigItem = ConfigItem("asr", "asr_type", "baidu")

    tts_list: list = ['edgetts', 'cosyvoice', 'GPTSoVITS']
    tts: ConfigItem = ConfigItem("tts", "tts", False, BoolValidator())
    tts_type: OptionsConfigItem = OptionsConfigItem("tts", "tts_type", "GPTSoVITS", OptionsValidator(tts_list))
    tts_stream: ConfigItem = ConfigItem("tts", "tts_stream", False, BoolValidator())

    llm_list: list = ['qwen', 'fake']
    llm_type: OptionsConfigItem = OptionsConfigItem("llm", "llm_type", "fake", OptionsValidator(llm_list))
    # llm_type: ConfigItem = ConfigItem("llm", "llm_type", "qwen")
    llm_current_prompt_name: ConfigItem = ConfigItem("llm", "llm_current_prompt", "")
    audio_volume: RangeConfigItem = RangeConfigItem("audio", "audio_volume", 100, RangeValidator(0, 100))
    language_list: list = [f.split('.')[0] for f in os.listdir(i18n.get_lang_dir()) if f.endswith('.lang')]
    language: OptionsConfigItem = OptionsConfigItem("application", "language", "en_us", OptionsValidator(language_list))

    def setup(self):
        self.slotConnectSignal()
        i18n.set_language(self.language.value)




    def slotConnectSignal(self):
        self.language.valueChanged.connect(i18n.set_language)




