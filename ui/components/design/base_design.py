import os.path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import SingleDirectionScrollArea


class BaseDesign(QWidget):
    resource_dir: str

    def __init__(self):
        super().__init__()
        mainLayout = QVBoxLayout()
        scrollArea = SingleDirectionScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("QScrollArea{background: transparent; border: none}")
        # 滚动区域内控件
        view = QWidget()
        view.setStyleSheet("QWidget{background: transparent}")
        self.vLayout = QVBoxLayout(view)
        scrollArea.setWidget(view)
        mainLayout.addWidget(scrollArea)
        self.setLayout(mainLayout)
        self.vLayout.setContentsMargins(10, 10, 10, 10)


class IconDesign:
    resource_dir: str
    def icon(self, path: str):
        return QIcon(os.path.join(self.resource_dir.rsplit("/", maxsplit=1)[0], path))