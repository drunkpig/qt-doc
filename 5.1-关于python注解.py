"""
1，decorator的本质
2，普通装饰器与带参装饰器
3，如何兼容带参与不带参
4，作用在类上的装饰器

"""
################################################################
# 一个普通的decorator
################################################################
import functools


def my_docorator(func):
    def inner_func(*args, **kwargs):
        print("调用前")
        rtn = func(*args, **kwargs)
        print("调用之后")
        return rtn
    return inner_func


"""
有一些装饰器会带括号、参数等。实际上不带括号的很直接就是个接受一个function参数的函数名字；
那么如果有括号就相当于是执行一个函数（带参或者不带参）得到其返回值然后再作用在被装饰的函数上；
结论：无论@后面这一坨怎么写，最终它都要返回一个只接受函数参数的函数
"""
@my_docorator
def myfunc(name):
    print(f"name={name}")


myfunc("cxu")

"""
输出为
--------------
调用前
name=cxu
调用之后
--------------
"""


################################################################
# 1.docorator的本质
################################################################
"""
以上调用myfunc("cxu")可以等价于下面的代码
"""


def myfunc2(name):
    """这里新写个函数是因为上面的myfun已经被装饰过了，新写个没有被装饰过的"""
    print("myfunc2: ", name)


print("这是本质输出：-------------")
# 下面一句相当于把 @之后的表达式当成一个变量来求，得到一个以函数为参数的函数。
# 理解这个地方非常重要，可以解释为什么有的装饰器可以不加括号，有的必须加括号，有的装饰器还可以有参数。
# 实际上没有加括号的就是一个最终变量，其形式必须是接受一个函数参数。
# 如果是@有括号的，则代表了是对表达式求值，这个值最终也是一个接受函数参数的函数。
decorator_func = my_docorator
new_func = decorator_func(myfunc2) # 然后生成一个新的函数
new_func("cxu")  # 调用这个新的函数


################################################################
# 2. 带参/括号装饰器
################################################################

def mydocorator3(arg1, arg2, arg3):
    print(f"arg1={arg1}, arg2={arg2}, arg3={arg3}")
    def func3(func):
        def inner(*args, **kwargs):
            print("调用之前")
            val = func(*args, **kwargs)
            print("调用之后")
            return val
        return inner
    return func3


@mydocorator3("A", "B", "C")
def myfunc3(name):
    print("myfunc3 name=", name)


myfunc3("myfunc3_name")


################################################################
# 3. 如何兼容带参与不带参
################################################################
"""
有的时候为了使用方便比如下面几种情形
@mydecorator
@mydecorator()
@mydecorator(name='张三')

那么如何实现这种装饰器呢？
"""


def repeat(_func=None, *, num_times=2):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat

    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)


@repeat # 不加括号
def say_whee():
    print("Whee!")


@repeat() # 加括号
def say_sth():
    print("say sth")


@repeat(num_times=3) # 括号带参
def greet(name):
    print(f"Hello {name}")


say_whee()
greet("老王")
say_sth()


################################################################
# 4. 作用在类上的参数
################################################################
"""
所有作用在函数上的也能作用在类上，只不过参数成了一个类（注意不是类实例）。

"""


print("作用在类上的装饰器--------------------------")


def timer(func):
    def timeit(*args, **kwargs):
        print("开始调用")
        rtn = func(*args, **kwargs)
        print("结束调用，耗时X秒")
        return rtn
    return timeit


@timer
class TimeWaster:
    def __init__(self, max_num):
        self.max_num = max_num

    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i**2 for i in range(self.max_num)])


x = TimeWaster(1) # 这里会有打印
x.waste_time(2) # 这里装饰器不起任何作用。也就是作用在类上的装饰器只作用于构造函数之上

#######################
# 下面几个场景如何实现
# 1. 构造类之后调用类里某个函数，或者其他函数
# 2. decorator如何get到self?
# 3. 作用在类属性上的装饰器，如何自动调用这个属性的某个方法？
# 4.
#######################

print("------展示改造类的构造行为-------")


def class_wrapper(cls):
    def wapper(*args, **kwargs):
        print("开始构造")
        rtn = cls(*args, **kwargs)
        print("结束构造，耗时X秒")
        rtn.name = "李四" # 这个地方可以对这个构造好的实例进行编辑
        rtn.hehe() # 直接调用类实例方法，这也解释了如何获取到self
        return rtn
    return wapper


@class_wrapper
class ClassA:

    def __init__(self, name):
        self.name = name
        print("我是类的构造函数, name=", self.name)

    def say_hello(self):
        print("我名字是：", self.name)

    def hehe(self):
        print("呵呵")


cls = ClassA("张三")
cls.say_hello() # 理论上来说这里应该输出的名字为张三，但是由于使用了装饰器，被修改为李四


print("------------装饰器作用在类属性上-----------")


def property_wrapper(cls):
    def wapper(*args, **kwargs):
        print("开始构造")
        cls.set_age(18)
        print("结束构造，耗时X秒")
    return wapper


class ClassC:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def set_age(self, age):
        self.age = age
        print(f"年龄被设置为{age}岁")


class ClassB:

    def __init__(self, name):
        #@property_wrapper   # 如果直接这么写，ERROR: @ or def expected， 说明python语法上并不支持
        self.p = ClassC(name, 0) # 希望通过装饰器能够让p的年龄为18岁
        print("我是类的构造函数, age=", self.p.age)

    def say_hello(self):
        print("我年龄是：", self.p.age)

"""
思考：如果不能使用属性上的装饰器，那么怎么办？
思路：利用class上的装饰器结合反射，详细参考5.2和5.3
"""

#######################################
# 几个很方便写装饰器的库
# https://pypi.org/project/decorator/
# https://pypi.org/project/decorators/
# https://wiki.python.org/moin/PythonDecoratorLibrary
# Awesome Python Decorator https://github.com/lord63/awesome-python-decorator
#######################################
