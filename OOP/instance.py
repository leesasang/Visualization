import types

class MyClass:
    def __init__(self, x):
        self.x = x

def greet(self):
    print(f"Hello, {self.x}")

# ================
# instance variable 또는 instance attribute를 동적으로 추가.
obj0 = MyClass("dynamic_attri")
obj0.y = 100
print(f"{obj0.y = }")

del obj0.y

# ================
# Special Case
# 특정 instance에만 instance method를 추가.
obj = MyClass("test")
obj.greet = types.MethodType(greet, obj)
# greet는 obj에 binding된 bound method가 되며, obj에서만 사용 가능.

obj.greet()
del obj.greet

# n_obj = MyClass("new")
# n_obj.greet()  # error! greet는 obj에만 추가되었으므로 n_obj에서는 사용할 수 없음.

# ================
# instance method를 class에 동적으로 추가.
MyClass.greet1 = greet

obj1 = MyClass("obj1")
obj1.greet1()
obj.greet1()

# ================
# class method를 class에 동적으로 추가.
def desc(cls):
    print(f"This is {cls.__name__}")

MyClass.desc = classmethod(desc)

MyClass.desc()
obj.desc()

# ================
# static method를 class에 동적으로 추가.
def copyright():
    print("GPL!")

MyClass.copyright = staticmethod(copyright)

MyClass.copyright()
obj.copyright()
