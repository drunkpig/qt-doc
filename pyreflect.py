"""
反射：
1：从父类，反射出儿子里新定义的属性和方法
2：从父类，反射出父类自己的属性和方法
3：从父类，反射出儿子里覆盖的方法和属性

4：从子类，反射出父类独有属性和方法
5：从子类，反射出自己的属性和方法
6：从子类，反射出爷爷的属性和方法
TODO
"""

def inspect_1(clz):
    class inspect_(clz):
        def __init__(self, *args, **kwargs):
            self._decor = "我是装饰器类"
            super().__init__(*args, **kwargs)
            print(vars(self))
            print(dir(self))
            print(self.__mro__)

    return inspect_


class Annimal(object):
    def __init__(self, cls):
        self.cls = cls

    def say(self):
        print("wawawa!!!!")

    def live(self):
        print("live")

@inspect_1
class Person(Annimal):
    def __init__(self, name:str, age:int):

        self.name = name
        self.age = age
        super().__init__("HUMAN")

    def say(self):
        print("你好")

    def dance(self):
        print('dance')


class Man(Person):
    def __init__(self, gender, name:str, age:int):
        self.gender = gender
        super().__init__(name, age)


if __name__=="__main__":
    p = Person("lili", 18)
    p.say()