from threading import Thread, Lock
import time


def x_plus_y(x: int, y: int, x_lock: Lock, y_lock:Lock):
    while True:
        x_lock.acquire()
        y_lock.acquire()
        print(f"Sum of x and y {x + y}")
        time.sleep(0.1)
        y_lock.release()
        x_lock.release()

def y_times_x(y: int, x: int, y_lock: Lock, x_lock: Lock):
    while True:
        y_lock.acquire()
        x_lock.acquire()
        print(f"Product of y and x {y * x}")
        time.sleep(0.1)
        y_lock.release()
        x_lock.release()

def example5():
    '''This example is showing a deadlock where two threads are 
    competing with two locks. Let's debug it'''
    x = 4
    y = 3
    x_lock = Lock()
    y_lock = Lock()
    thread1 = Thread(name="X + Y", target=x_plus_y, args=(x, y, x_lock, y_lock))
    thread2 = Thread(name="Y + X", target=y_times_x, args=(y, x, y_lock, x_lock))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
