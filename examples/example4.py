from threading import Thread, Lock
import time

i = 0

mutex_lock = Lock()

def increment_even_numbers():
    global i
    global mutex_lock
    while i < 40:
        mutex_lock.acquire(blocking=True)
        print("Even thread acquired lock")
        if i & 1 != 1:
            print(f"Updating even number. Before {i}", end='')
            i += 1 
            print(f" and after {i}")
        print("Even thread releasing lock")
        mutex_lock.release()
        
        time.sleep(0.5)

def increment_odd_numbers():
    global i
    global mutex_lock
    try:
        while i < 40:
            mutex_lock.acquire(blocking=True)
            print("Odd thread acquired lock")
            if i & 1 == 1:
                print(f"Updating odd number. Before {j}", end='')
                i += 1 
                print(f" and after {i}")
            print("Odd thread releasing lock")
            mutex_lock.release()

            time.sleep(0.5)
    except Exception as e:
        print("whoopsie")

def monitor_number():
    global i
    while i < 40:
        print(f"Current number status: {i}")
        time.sleep(5)

def example4():
    '''This example is not allowing all threads to continue. Let's fix that'''

    thread1 = Thread(name="Even numbers", target=increment_even_numbers)
    thread2 = Thread(name="Odd numbers", target=increment_odd_numbers)
    thread3 = Thread(name="Number monitoring", target=monitor_number)

    print()

    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
