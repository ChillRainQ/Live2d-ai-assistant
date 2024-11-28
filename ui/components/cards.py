from typing import Union

from PySide6.QtGui import QIcon
from qfluentwidgets import SettingCard, RangeConfigItem, SpinBox


class Card(SettingCard):
    def __init__(self, icon, title):
        super().__init__(icon, title)
        self.setContentsMargins(10, 10, 10, 10)

class RangeItemSettingCard(Card):
    def __init__(self, configItem: RangeConfigItem, icon: Union[str, QIcon], title: str):
        super().__init__(icon, title)
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


