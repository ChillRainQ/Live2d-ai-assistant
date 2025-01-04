from PySide6.QtGui import QIcon
from qfluentwidgets import SettingCard, RangeConfigItem, SpinBox, ConfigItem, ComboBox, FluentIconBase, DoubleSpinBox


class Card(SettingCard):
    def __init__(self, icon, title, content=None):
        super().__init__(icon, title, content)
        self.setContentsMargins(10, 10, 10, 10)


class RangeItemSettingCard(Card):
    def __init__(self, configItem: RangeConfigItem, icon: str | QIcon | FluentIconBase, title: str, content=None):
        super().__init__(icon, title, content)
        self.configItem = configItem
        box = SpinBox()
        box.setMinimumWidth(150)
        box.setSingleStep(10)
        box.setRange(*configItem.range)
        box.setValue(configItem.value)
        self.hBoxLayout.addWidget(box)
        box.valueChanged.connect(self.setValue)

    def setValue(self, value):
        self.configItem.value = value

class RangeDoubleItemSettingCard(Card):
    def __init__(self, configItem: RangeConfigItem, icon: str | QIcon | FluentIconBase, title: str, content=None):
        super().__init__(icon, title, content)
        self.configItem = configItem
        box = DoubleSpinBox()
        box.setMinimumWidth(150)
        box.setSingleStep(0.1)
        box.setRange(*configItem.range)
        box.setValue(configItem.value)
        self.hBoxLayout.addWidget(box)
        box.valueChanged.connect(self.setValue)

    def setValue(self, value):
        self.configItem.value = value


class SelectSettingCard(Card):
    def __init__(self, configItem: ConfigItem, selectList: list, icon: str | QIcon | FluentIconBase, title: str, content=None):
        super().__init__(icon, title, content)
        self.config = configItem
        self.selectList = selectList
        self.cb = ComboBox()
        self.cb.addItems(self.selectList)
        self.cb.currentTextChanged.connect(self.changeValue)
        self.cb.setCurrentText(self.config.value)
        self.hBoxLayout.addWidget(self.cb)
        self.hBoxLayout.addSpacing(10)

    def changeValue(self):
        self.config.value = self.cb.currentText()
