"""
定义一个minawindows, 上面有2个按钮。
按钮的初始化文本都是“testme"。
当点击其中一个按钮的时候，另一个按钮的文本改变为一个随机的整数。
"""
import random

from PySide2 import QtCore
from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QPushButton, QMainWindow, QApplication


class MyBtn1(QPushButton):
    SigBtn1Clicked = Signal(str)

    def __init__(self, parent, objectName):
        super(MyBtn1, self).__init__(parent, objectName=objectName)
        self.setText("testme")
        QtCore.QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_btn2_clicked(self):
        self.setText(str(random.randint(0, 100)))
        self.SigBtn1Clicked.emit(self.text())

    @Slot(str)
    def on_btn2_SigBtn2Clicked(self, text):
        print("MyBtn1:", text)


class MyBtn2(QPushButton):
    SigBtn2Clicked = Signal()

    def __init__(self, parent, objectName):
        super(MyBtn2, self).__init__(parent, objectName=objectName)
        self.setText("testme")
        QtCore.QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_btn1_clicked(self):
        self.setText(str(random.randint(0, 100)))
        self.SigBtn2Clicked.emit(self.text())

    @Slot(str)
    def on_btn1_SigBtn1Clicked(self, text):
        print("MyBtn2:", text)


class MainWindow(QMainWindow):
    """
    这种写法毫无疑问是没有问题的。
    """

    def __init__(self, title="title"):
        super().__init__()
        self.setWindowTitle(title)
        self.btn1 = MyBtn1(self, "btn1")
        self.btn2 = MyBtn2(self, "btn2")
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.btn1.setGeometry(10, 10, 100, 30)
        self.btn2.setGeometry(10, 50, 100, 30)

    def btn1_clicked(self):
        self.btn2.setText(str(random.randint(1, 100)))

    def btn2_clicked(self):
        self.btn1.setText(str(random.randint(1, 100)))


class MainWindow2(QMainWindow):
    def __init__(self, title="title"):
        super().__init__()
        self.setWindowTitle(title)
        """
        现在bt1和bt2是同一个窗口中的平行的组件。那么他们之间可以对对方的信号进行连接吗。
        """
        self.btn1 = MyBtn1(self, objectName="btn1")
        self.btn2 = MyBtn2(self, objectName="btn2")
        self.btn1.setGeometry(10, 10, 100, 30)
        self.btn2.setGeometry(10, 50, 100, 30)
        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainwindow = MainWindow2("windows_1")
    mainwindow.show()

    sys.exit(app.exec_())
