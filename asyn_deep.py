import time
from itertools import cycle

def easy_range(n):
    i = 0
    while i < n:
        t = yield i
        if t is None:
            pass
        else:
            i = t
        i += 1


def add_hello():
    while True:
        x = (yield)
        return ("Hello " + x)

def writer_wrapper():
    i = yield from add_hello()
    i += " Hello"
    return i

w = writer_wrapper()
next(w)
try:
    print(w.send("World"))
except StopIteration as e:
    print(e.value)
    
my_range = easy_range(10)
print(next(my_range))
print(next(my_range))
print(my_range.send(4))

def async_sleep():
    return (yield)

def async_print():
    print("One")
    while True:
        yield from async_sleep()
        print("Two")

task = [async_print() for _ in range(2)]

for i in task:
    next(i)

time.sleep(1)

for i in task:
    next(i)
