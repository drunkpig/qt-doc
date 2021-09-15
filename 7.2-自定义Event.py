"""
1. 利用event生成新事件, label的doubleClick
"""
from PySide2.QtWidgets import QLabel
import PySide2
from PySide2.QtCore import QEvent, Signal
from PySide2.QtGui import QKeyEvent, QMouseEvent

from qtdecorator import autoconnect

import sys

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication, QWidget


class Mylabel(QLabel):
    """
    label是没有double click行为的
    """
    clicked = Signal() # 自定义一个不存在的信号
    doubleClicked = Signal()

    def __init__(self, text):
        super().__init__(text)

    def event(self, evt:QEvent) -> bool:
        """
        函数返回TRUE表示event被正确处理了，否则表示没有被处理
        :param evt:
        :return:
        """
        if isinstance(evt, QMouseEvent) and evt.type()==QMouseEvent.MouseButtonRelease:
            evt.accept() # 这个地方直接拦截了，父亲得不到， 信号不起作用
            print(f"clicked emited")
            self.clicked.emit() # 或者这里可以发出一个自定义的信号了
            return True # 返回True代表事件已经被处理了，否则还是会进行传播!!!
        else:
            return super().event(evt)

    def mouseDoubleClickEvent(self, event:PySide2.QtGui.QMouseEvent) -> None:
        """
        如果去掉这个函数，label将不会对双击事件做出回应
        :param event:
        :return:
        """
        self.doubleClicked.emit()
        print("doubleClicked emited")


@autoconnect
class UIMyEditorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self):
        layout = QVBoxLayout()
        self.lb = Mylabel("click me")
        self.lb.setObjectName("lb")   # TODO autoconnect 装饰器有个小bug,导致不能扫描出本类定义的Qobject,名字没有设置成功
        layout.addWidget(self.lb)

        self.setLayout(layout)

    def event(self, evt:QEvent) -> bool:
        if isinstance(evt, QMouseEvent) and evt.type()==QMouseEvent.MouseButtonRelease:
            print(f"父亲得到{evt.type()}")
            return True
        else:
            return super().event(evt)


class MyEditorDialog(UIMyEditorDialog):
    def __init__(self, parent):
        super().__init__(parent)

    @QtCore.Slot()
    def on_lb_clicked(self):
        print("clicked action")

    @QtCore.Slot()
    def on_lb_doubleClicked(self):
        print("double clicked action")


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = MyEditorDialog(None)
    dialog.show()
    qtapp.exec_()



