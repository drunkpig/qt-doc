from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QGroupBox, QPlainTextEdit, QHBoxLayout, QCheckBox, \
    QRadioButton, QLabel, QFormLayout, QLineEdit, QSpinBox, QWidget
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
        self.result_label = QLabel("")
        self.result_label.setLineWidth(50)
        self.v_layout.addWidget(self.result_label)

        self.name_input = QLineEdit()
        self.name_input.setObjectName("nameInput")
        self.age_input = QSpinBox()
        self.age_input.setObjectName("ageInput")
        form_layout = QFormLayout() # 这个地方写成 QFormLayout(self)，这个layout自动被设置为了self的layout，这样界面其他组件不会显示
        form_layout.addRow("Name", self.name_input)
        form_layout.addRow("age", self.age_input)
        self.v_layout.addLayout(form_layout)

        self.setLayout(self.v_layout)

        self.setWindowTitle("自定义信号")

    def _set_label(self, msg):
        self.result_label.setText(msg)


class MyDialog(UIMyEditorDialog):

    oldmanFound = Signal(int, str) # 自定义信号

    def __init__(self, parent):
        super().__init__(parent)
        self.oldmanFound[int,str].connect(self.on_oldmanFound) # 这个地方目前还没发现可以自动connect

    @QtCore.Slot(str) # 在pyqt5中，这个注解可有可无，但是pyside2中一定需要，可见pyqt更成熟一些
    def on_nameInput_textChanged(self, new_text):
        """
        :param state:
        :return:
        """
        print("name：", new_text)

    @QtCore.Slot(int)
    def on_ageInput_valueChanged(self, val):
        print("age：", val)
        if val > 10:
            self.oldmanFound.emit(val, self.name_input.text())

    @QtCore.Slot(int, str) # 这一句注解可以去掉不影响结果，但是可读性变差了
    def on_oldmanFound(self, age, name):
        msg = f"old man found: age={age}, name={name}"
        print(msg)
        super()._set_label(msg)


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = MyDialog(None)
    dialog.show()
    qtapp.exec_()
