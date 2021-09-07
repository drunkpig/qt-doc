from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGroupBox, QPlainTextEdit, QHBoxLayout, QCheckBox, \
    QRadioButton, QSpinBox
import sys


class UIMyEditorDialog(QDialog):
    """
    总结要点：

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setup_ui()
        QtCore.QMetaObject.connectSlotsByName(self) # 这行代码写在父类还是子类对结果没有影响，那么写在父类里可以让逻辑部分更清晰

    def __setup_ui(self):
        self.v_layout = QVBoxLayout()
        self.ft_style_group = QGroupBox()
        self.color_group = QGroupBox()
        self.editor = QPlainTextEdit()
        self.spinBox = QSpinBox(self)
        self.spinBox.setObjectName("spinBox")

        self.v_layout.addWidget(self.editor)
        self.v_layout.addWidget(self.ft_style_group)
        self.v_layout.addWidget(self.color_group)
        self.v_layout.addWidget(self.spinBox)
        self.setLayout(self.v_layout)

        self.ft_style_layout = QHBoxLayout()
        self.italicCheckbox = QCheckBox("斜体", self)
        # 这句话真的不能少！！靠变量名字达不到效果，不妨尝试用一个注解来实现，这样代码更简洁+清晰
        # 这个代码设置了这个italicCheckbox的名字，通过和QtCore.QMetaObject.connectSlotsByName的结合达到自动连接槽函数的目的。
        self.italicCheckbox.setObjectName("italicCheckbox")
        self.bold_checkbox = QCheckBox("粗体",self)
        self.underline_checkbox = QCheckBox("下划线",self)
        self.ft_style_layout.addWidget(self.italicCheckbox)
        self.ft_style_layout.addWidget(self.bold_checkbox)
        self.ft_style_layout.addWidget(self.underline_checkbox)
        self.ft_style_group.setLayout(self.ft_style_layout)

        self.color_layout = QHBoxLayout()
        self.red_radio = QRadioButton("红色", self)
        self.green_radio = QRadioButton("绿色", self)
        self.blue_radio = QRadioButton("蓝色", self)
        self.color_layout.addWidget(self.red_radio)
        self.color_layout.addWidget(self.green_radio)
        self.color_layout.addWidget(self.blue_radio)
        self.color_group.setLayout(self.color_layout)


class MyDialog(UIMyEditorDialog):
    def __init__(self, parent):
        super().__init__(parent)

    @QtCore.pyqtSlot(bool)
    def on_italicCheckbox_clicked(self, is_checked):
        """
        这个函数也不会起作用的，Slot并不支持无参函数
        :return:
        """
        print("italicCheckbox clicked ",  is_checked)

    ##################################################################
    # 下面2个函数会同时执行，也就是一个signal会同时发给这2个函数。这是pyside2目前无法做到的。
    @QtCore.pyqtSlot(int, name="on_spinBox_valueChanged")
    def spinBox_valueChanged_int(self, int_val):
        print("on_spinBox_valueChanged_int ", int_val)

    @QtCore.pyqtSlot(str, name="on_spinBox_valueChanged")
    def spinBox_valueChanged_str(self, str_val):
        print("on_spinBox_valueChanged_str ", str_val)

    ###################################################################


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = MyDialog(None)
    dialog.show()
    qtapp.exec_()
