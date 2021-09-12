"""
场景：
有2个按钮，一个代表红色，一个打标蓝色。
这2个按钮都连接到1个slot上，slot需要知道发生点击时到底是哪个按钮被点击了。
"""
import sys
from functools import partial

from PySide2.QtWidgets import QVBoxLayout, QDialog
from PySide2 import QtCore
from PySide2.QtWidgets import QWidget, QPushButton, QApplication


class UIMywin(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setup_ui()
        self.__connect()

    def __setup_ui(self):
        self.red_btn = QPushButton("RED", self)
        self.green_btn = QPushButton("GREEN", self)
        layout = QVBoxLayout()
        layout.addWidget(self.red_btn)
        layout.addWidget(self.green_btn)
        self.setLayout(layout)
        self.setMinimumWidth(200)

    def __connect(self):
        # 方式1：lambda表达式
        self.red_btn.clicked.connect(lambda :self.on_btn_clicked("RED"))
        # 方式2：使用partial
        self.green_btn.clicked.connect(partial(self.on_btn_clicked, "GREEN"))

    def on_btn_clicked(self, btn_name):
        print(f"button {btn_name} clicked")


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = UIMywin(None)
    dialog.show()
    qtapp.exec_()