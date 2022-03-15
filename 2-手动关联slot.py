from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QGroupBox, QPlainTextEdit, QHBoxLayout, QCheckBox, \
    QRadioButton, QSpinBox
import sys


class UIMyEditorDialog(QDialog):
    """
    总结要点：
    pyside2还无法像pyqt一样使用Slot(, name="on_objName_signal")来重载slot, 让2个slot同时执行
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setup_ui()

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
        self.italicCheckbox.clicked.connect(self.on_italicCheckbox_clicked) # 斜体手动关联
        self.spinBox.valueChanged[str].connect(self.on_spinBox_valueChanged_1)# pyside2虽然不支持QtCore.Slot中name参数重载，但是手工还是可以实现的
        self.spinBox.valueChanged[int].connect(self.on_spinBox_valueChanged_2) # 点击spinBox，这2个都会被触发

        # 下面这个执行时报错：IndexError: Signature valueChanged(int,QString) not found for signal: valueChanged
        # self.spinBox.valueChanged[int,str].connect(self.on_spinBox_valueChanged_2)

    def on_italicCheckbox_clicked(self, is_checked):
        """
        :return:
        """
        print("italicCheckbox clicked ",  is_checked)


    def on_spinBox_valueChanged_1(self, str_val:str):
        """
        :param str_val:
        :return:
        """
        print("on_spinBox_valueChanged_str ", str_val)

    def on_spinBox_valueChanged_2(self, int_val:int):
        """
        :param int_val:
        :return:
        """
        print("on_spinBox_valueChanged_int ", int_val)

    def on_spinBox_valueChanged_3(self, int_val:int, str_val:str):
        """
        这个在执行时connect会绑定不成功，因为没有满足这个参数的列表的signal
        :param int_val:
        :return:
        """
        print("on_spinBox_valueChanged_int ", int_val, str_val)


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = MyDialog(None)
    dialog.show()
    qtapp.exec_()
