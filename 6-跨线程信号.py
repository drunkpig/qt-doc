import sys
import time

from PySide2 import QtCore
from PySide2.QtCore import QThread, Signal, QDateTime
from PySide2.QtWidgets import QDialog, QLineEdit, QApplication


class BackendThread(QThread):
    def __init__(self, parent):
        super().__init__(parent) # 注意如果要实现自动连接，设置parent非常重要。
    # 通过类成员对象定义信号
    updateDate = Signal(str)

    # 处理业务逻辑
    def run(self):
        while True:
            data = self.__do_compute_intensive_task()
            self.updateDate.emit(data)

    def __do_compute_intensive_task(self):
        """
        这里模拟一个耗时的计算，如果在界面逻辑里直接做会导致界面卡顿。
        :return:
        """
        data = QDateTime.currentDateTime()
        curr_time = data.toString("yyyy-MM-dd hh:mm:ss")
        time.sleep(1)
        return str(curr_time)


class UIWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __init_ui(self):
        self.resize(400, 100)
        self.input = QLineEdit(self)
        self.input.resize(400, 100)
        # 创建线程
        self.backend = BackendThread(self)
        self.backend.setObjectName("backendThread")
        # 连接信号
        #self.backend.updateDate.connect(self.on_backendThread_updateDate)
        # 开始线程
        self.backend.start()


class Winidow(UIWindow):
    def __init__(self):
        super().__init__()

    @QtCore.Slot(str)
    def on_backendThread_updateDate(self, data): # 将当前时间输出到文本框
        self.input.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Winidow()
    win.show()
    sys.exit(app.exec_())


