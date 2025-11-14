from threading import Thread
import time

i = 0

def foo():
    global i
    while i < 40:
        print(f"Hello world - count {i}")
        i +=1 
        time.sleep(0.5)

def example2():
    '''This example is not protecting access to the resource it is using. Let's fix that'''

    thread1 = Thread(name="This is number one", target=foo)
    thread2 = Thread(name="And then this is number two", target=foo)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
