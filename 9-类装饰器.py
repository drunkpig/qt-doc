"""
https://stackoverflow.com/questions/7477311/inheriting-from-decorated-classes
https://realpython.com/primer-on-python-decorators/#decorating-classes

"""


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