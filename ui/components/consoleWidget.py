from PySide6.QtCore import Qt
from PySide6.QtGui import QTextBlockFormat, QFont, QTextOption
from PySide6.QtWidgets import QTextEdit

from config.application_config import ApplicationConfig
from ui.components.design.base_design import BaseDesign


class ConsoleWidget(BaseDesign):
    def __init__(self, config: ApplicationConfig):
        BaseDesign.__init__(self, config)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        format = QTextBlockFormat()
        format.setLineHeight(7, 2)
        option = QTextOption()
        option.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.text.document().setDefaultTextOption(option)
        self.text.document().setDefaultTextOption(option)
        cursor = self.text.textCursor()
        cursor.setBlockFormat(format)
        self.text.setTextCursor(cursor)
        self.write("\n")
        self.vLayout.addWidget(self.text)
        self.setObjectName('console')



    def write(self, message: str):
        self.text.append(message)
