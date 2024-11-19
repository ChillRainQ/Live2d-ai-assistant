from qfluentwidgets import SettingCard


class Card(SettingCard):
    def __init__(self, icon, title):
        super().__init__(icon, title)
        self.setContentsMargins(10, 10, 10, 10)

class SingleSettingCard(Card):
    pass

# class