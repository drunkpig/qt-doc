"""
由于实例化一个控件之后，还要设置其objectName才能实现自动绑定。
本代码实现一种利用类上的注解来实现自动设置objectName， 使用注解的好处是代码清晰，明显看到某个控件具有自动连接特性。
"""

def my_decorator(max):
    print("max=", max)
    def wrapper(func):
        print("do somth")

        def myfunc(*args, **kwargs):
            func(*args, **kwargs)
        return myfunc

    return wrapper


@my_decorator(max=10)
def say_me(name):
    print("syame ", name)


if __name__=='__main__':
    say_me('jon')
