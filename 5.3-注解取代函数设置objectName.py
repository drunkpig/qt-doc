"""
由于实例化一个控件之后，还要设置其objectName才能实现自动绑定。
本代码实现一种利用类上的注解来实现自动设置objectName， 使用注解的好处是代码清晰，明显看到某个控件具有自动连接特性。
"""

"""
实现qt类装饰器，具备功能：
1，自动扫描类中控件，自动设置objectName

"""
import sys

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication

def inject_class(mixin):
    def _inject_class(cls):
        return type(cls.__name__,(mixin,)+cls.__bases__,dict(cls.__dict__))
    return _inject_class

class MixIn(object):
    def mix(self):
        print('mix')

@inject_class(MixIn)
class Foo(object):
    def foo(self):
        print('foo')

class Goo(Foo):
    def goo(self):
        print('goo')

goo=Goo()
goo.mix()
goo.foo()
goo.goo()




