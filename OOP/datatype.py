class Samp1:
    pass

def Func1():
    pass

a = Samp1()
b = Func1

c = 7

print(f"a's type: {type(a)}")         # a's type: <class '__main__.Samp1'>
print(f"Samp1's type: {type(Samp1)}") # Samp1's type: <class 'type'>

print(f"Func1's type: {type(Func1)}") # Func1's type: <class 'function'>
print(f"b's type: {type(b)}")         # b's type: <class 'function'>

print(f"Literal 7's type: {type(7)}") # Literal 7's type: <class 'int'>
print(f"c's type: {type(c)}")         # c's type: <class 'int'>
print(f"int's type: {type(int)}")     # int's type: <class 'type'>
