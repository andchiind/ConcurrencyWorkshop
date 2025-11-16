from random import random, randrange
from threading import Thread
import time
from typing import List

class BitThread(Thread):
    def __init__(self, index: int):
        self.flag: bool = False
        Thread.__init__(self, name=f"Bit thread {index}")
    
    def flip_flag(self):
        self.flag = not self.flag
        return self.flag

    def run(self):
        while True:
            if random() > 0.95: # Cosmic rays
                self.flip_flag()

class CoordinatorThread(Thread):
    def __init__(self):
        self.flags: List[bool] = []
        Thread.__init__(self, name=f"Coordinator thread")
    
    def run(self):
        while True:
            time.sleep(0.5)

class UserThread(Thread):
    def __init__(self, index: int):
        Thread.__init__(self, name=f"User thread {index}")
    
    def run(self):
        number_of_flags = 10
        while True:
            # Randomly decide if we want to flip a flag
            if random() > 0.6:
                # Randomly select which flag to flip from a uniform distribution
                index_to_flip = randrange(0, number_of_flags - 1)
            time.sleep(2)


def many_to_one_to_many():
    '''In this example we want to design a system letting the User threads
    get an updated and consistent state of the bit flag values set by the
    Bit threads, while also being able to request to change the values.'''
    number_of_threads = 5

    bit_threads = []
    for i in range(number_of_threads):
        bit_thread = BitThread(i)
        bit_thread.start()
        bit_threads.append(bit_thread)

    coordinator = CoordinatorThread()
    coordinator.start()

    user_threads = []
    for i in range(number_of_threads):
        user_thread = UserThread(i)
        user_thread.start()
        user_threads.append(user_thread)

    coordinator.join() # Keeps the main thread alive
