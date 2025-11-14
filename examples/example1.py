from threading import Thread
import time

def example1():
    '''This example will never end. Let's try close them from the parent'''
    def foo():
        i = 0
        while True:
            print(f"Hello world - count {i}")
            i +=1 
            time.sleep(1)

    thread1 = Thread(name="This is number one", target=foo)
    thread2 = Thread(name="And then this is number two", target=foo)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
