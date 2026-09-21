# in built libraries

import math

print(math.sqrt(9))
print(math.ceil(4.2))
print(math.floor(4.2))

import random  

print(random.randint(11, 30))

from datetime import datetime

current_time = datetime.now()
print("Current date and time: ", current_time)

# __name__ == "__main__"

def myfunc1():
    print("Hi, my name is Vikash")

def myfunc2():
    print("Vikash likes pixar movies")

def myfunc3():
    print("Vikash likes to eat momos on weekend.")

print("Going to my neighbor...")
print(__name__)

if __name__ == "__main__":
    myfunc1()
    myfunc2()
    myfunc3()