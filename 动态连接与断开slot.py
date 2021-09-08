"""
一共2个按钮，第一个有响应，第二个无响应。
点击第一个之后立刻“死去”，第二个开始有响应。
点击第二个之后立刻“死去”， 切换到第一个开始有响应。

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
        self.red_btn = QPushButton("第一个按钮", self)
        self.green_btn = QPushButton("第二个按钮", self)
        self.btns = [self.red_btn, self.green_btn]
        layout = QVBoxLayout()
        layout.addWidget(self.red_btn)
        layout.addWidget(self.green_btn)
        self.setLayout(layout)
        self.setMinimumWidth(200)

    def __connect(self):
        # 激活第一个按钮
        self.__do_connect(0)

    def __do_connect(self, i):
        mybtn = self.btns[i]
        mybtn._con = lambda: self.on_btn_clicked(mybtn.text()) # 这点也很重要，暂存lambda或者partil构成的函数，否则临时函数无法解除连接
        mybtn.con = mybtn.clicked.connect(mybtn._con)

    def __do_discon(self, i):
        mybtn = self.btns[i]
        mybtn.clicked.disconnect(mybtn._con)

    def __switch_connect(self, i):
        """
        激活第i个，其他断开
        :param i:
        :return:
        """
        self.__do_connect(i)
        self.__do_discon(abs(i-1))

    def on_btn_clicked(self, btn_name):
        print(f"button {btn_name} clicked")
        if btn_name=="第一个按钮":
            self.__switch_connect(1)
        else:
            self.__switch_connect(0)


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = UIMywin(None)
    dialog.show()
    qtapp.exec_()