from threading import Thread, Lock
import time
from typing import List


def run_print_index_sum(locks: List[Lock], indices: List[int]):
    '''This function prints the sum of the given list of indices, respecting
    the lock for all the preceding elements in the list'''
    assert len(locks) == len(indices)
    while True:
        print_index_sum(locks, indices, 0, 1)


def print_index_sum(locks: List[Lock], indices: List[int], sum, depth):
    '''This function acquires the lock at the current list index, then either
    prints out the current index sum, or recursively progresses down the list'''
    time.sleep(0.1)  # This actually makes the issue less noticeable
    locks[-1].acquire()
    if len(locks) > 1:
        print_index_sum(locks[:-1], indices[1:], indices[0] + sum, depth + 1)
    else:
        print(f"The sum at index {depth} is {sum + indices[0]}")
    locks[-1].release()


def example4():
    """This example is showing starvation due to greedy threads. Let's fix that"""

    threads_n = 10

    shared_locks = [Lock() for i in range(threads_n)]

    threads = [
        Thread(
            name=f"Thread {i}",
            target=run_print_index_sum,
            args=(shared_locks[:i], range(i)),
        )
        for i in range(1, threads_n + 1)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()  # This will of course never stop blocking
