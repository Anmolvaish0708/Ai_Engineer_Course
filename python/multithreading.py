# multithreading

import time
import threading

# def task(name):
#     print(f"{name} started..")
#     time.sleep(3)
#     print(f"{name} finished.")

# start = time.time()

# task("Misc-Task1")
# task("Misc-Task2")
# task("Misc-Task3")
# task("Misc-Task4")
# task("Misc-Task5")

#end = time.time()

#print("Normal execution time:", end-start)
    

# import threading    

# thread1 = threading.Thread(
#     target=task,
#     args = ("Task1",)
# )

# thread2 = threading.Thread(
#     target=task,
#     args = ("Task2",)
# )

# thread3 = threading.Thread(
#     target=task,
#     args = ("Task3",)
# )

# thread4 = threading.Thread(
#     target=task,
#     args = ("Task4",)
# )

# thread5 = threading.Thread(
#     target=task,
#     args = ("Task5",)
# )

# start = time.time()

# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()

# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()
# thread5.join()

# end = time.time()

# print("Normal execution time:", end-start)

# write a function that takes a list and prints each element with its index and then takes one second delay then print another element. call this function with three different list.

def my_function(list):
    for i, l in enumerate(list):
        print(i,l)
        time.sleep(1)

lists = [
    ["apple", "banana", "cherry"],
    [10, 20, 30],
    ["red", "green", "blue"],
]

threads = [
    threading.Thread(target=my_function, args=(items,))
    for items in lists
]

start = time.time()

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end = time.time()

print("Multithreaded execution time:", end - start)
