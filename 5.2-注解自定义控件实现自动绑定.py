"""
1, 自动绑定实现2个能力：第一自动开启QtCore.QMetaObject.connectSlotsByName(self)；第二自动设置object_name
2，2个按钮共用同一个slot， 第一个点击传参RED，第二个传参BLUE。
本代码演示装饰器自动调用QtCore.QMetaObject.connectSlotsByName
"""

import sys

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication
from qtdecorator import autowire


@autowire # 无需在每个地方都调用 QtCore.QMetaObject.connectSlotsByName(self)
class UIMyEditorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self):
        layout = QVBoxLayout()
        self.btn = QPushButton("click me")
        self.btn.setObjectName("btn") # 这里还有一个代码，比较多余
        layout.addWidget(self.btn)
        self.setLayout(layout)


class MyEditorDialog(UIMyEditorDialog):
    def __init__(self, parent):
        super().__init__(parent)

    @QtCore.Slot()
    def on_btn_clicked(self):
        print("clicked")


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = MyEditorDialog(None)
    dialog.show()
    qtapp.exec_()
