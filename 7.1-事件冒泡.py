"""
1, 事件冒泡，btn忽略，传给父亲
2， 父接受，传给子
3，信号连信号
"""
import PySide2
from PySide2.QtCore import QEvent
from PySide2.QtGui import QKeyEvent, QMouseEvent

from qtdecorator import autoconnect

import sys

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication, QWidget


class MyButton(QPushButton):
    """
    收到信号之后忽略送给父亲处理
    """
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
            print(f"子组件捕获{evt.type()}")
            self.click() # 或者这里可以发出一个自定义的信号了
            return True # 返回True代表事件已经被处理了，否则还是会进行传播!!!
        else:
            return super().event(evt)


@autoconnect
class UIMyEditorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self):
        layout = QVBoxLayout()
        self.whitepad = QWidget()
        self.whitepad.setLayout(layout)
        self.btn = MyButton("click me")
        layout.addWidget(self.btn)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.whitepad)
        self.setLayout(layout2)

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
    def on_btn_clicked(self):
        print("clicked")


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = MyEditorDialog(None)
    dialog.show()
    qtapp.exec_()


