"""
由于实例化一个控件之后，还要设置其objectName才能实现自动绑定。
本代码实现一种利用类上的注解来实现自动设置objectName， 使用注解的好处是代码清晰，明显看到某个控件具有自动连接特性。
"""
from qtdecorator import autoconnect

"""
实现qt类装饰器，具备功能：
1，自动扫描类中控件，自动设置objectName

"""
import sys

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication


@autoconnect
class UIMyEditorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self):
        layout = QVBoxLayout()
        self.btn = QPushButton("click me")
        #self.btn.setObjectName("btn") # 这行可以不用要了
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

