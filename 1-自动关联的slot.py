from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QGroupBox, QPlainTextEdit, QHBoxLayout, QCheckBox, \
    QRadioButton
import sys


class UIMyEditorDialog(QDialog):
    """
    总结要点：
    1）父类只负责组装界面，使用QtCore.QMetaObject.connectSlotsByName(self) 设置好自动槽函数关联机制
    2）父类创建的QT UI组件如果要有自动关联的槽函数需要使用setObjectName(name)设定一个实例的名字
    3）子类中实现逻辑处理slot函数，也就是界面点击所emit的signal。此时pyqt5和pyside2稍有区别：
       - pyqt5 的slot函数注解可有可无，但是pyside2中注解必须要有
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

        self.v_layout.addWidget(self.editor)
        self.v_layout.addWidget(self.ft_style_group)
        self.v_layout.addWidget(self.color_group)
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
        #QtCore.QMetaObject.connectSlotsByName(self)  # 这一行代码在父类写好之后，这里就不用再写

    @QtCore.Slot(int) # 在pyqt5中，这个注解可有可无，但是pyside2中一定需要，可见pyqt更成熟一些
    def on_italicCheckbox_stateChanged(self, state):
        """
        自动连接的槽函数，命名规则为  on_<object instance name>_<signal name>(<signal parameters>)
        :param state:
        :return:
        """
        print("stateChanged：", state)


if __name__=="__main__":
    qtapp = QApplication(sys.argv)
    dialog = MyDialog(None)
    dialog.show()
    qtapp.exec_()
