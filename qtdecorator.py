"""
实现qt类装饰器，具备功能：
1，作用在类上能够自动在构建类之后调用 QtCore.QMetaObject.connectSlotsByName(self)
2，扫描

"""
import inspect
import sys, pyreflect

from PySide2 import QtCore
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication


def autowire(clz):
    """
    可自动调用QtCore.QMetaObject.connectSlotsByName
    """
    class auto_wire(clz):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            QtCore.QMetaObject.connectSlotsByName(self)
    return auto_wire


def autoconnect(clz):
    """
    可以自动实现类中的slot和本类中的控件关联
    """
    def is_subclz(o, clz):
        instance_type = type(o).__name__
        # print(instance_type)
        b = isinstance(o, QPushButton)
        return b

    class auto_connect(clz):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # 开始扫描本类QObject子类，然后调用之上的setObjectName("控件名字")
            classes = inspect.getmembers(self, lambda o: is_subclz(o, QObject))
            for c in classes:
                obj_name = c[0]
                obj_instance = c[1]
                obj_instance.setObjectName(obj_name) # objectName就是变量的名字

            QtCore.QMetaObject.connectSlotsByName(self) # 这行代码必须写在setObjectName之后，否则也不起作用
    return auto_connect


@autoconnect
class UIMyEditorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self):
        layout = QVBoxLayout()
        self.btn = QPushButton("click me")
        # self.btn.setObjectName("btn") # 这一行也无需再写
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

