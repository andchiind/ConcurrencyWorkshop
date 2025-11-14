from threading import Thread
from dataclasses import dataclass
import time
from typing import Optional

@dataclass
class LinkedList:
    value: str
    next_element: Optional["LinkedList"] = None
    def __str__(self):
        return self.value + str(self.next_element) if self.next_element else ""

i = 0
my_name: LinkedList = LinkedList(
    value="A", 
    next_element=LinkedList(
        value="n",
        next_element=LinkedList(
            value="d",
            next_element=LinkedList(
                value="e",
                next_element=LinkedList(
                    value="r",
                    next_element=LinkedList(
                        value="s"))))))

def rename_to_sander():
    global my_name
    my_name.value = "S"
    my_name.next_element.value = "a"
    time.sleep(0)
    my_name.next_element.next_element.value = "n"
    my_name.next_element.next_element.next_element.value = "d"
    my_name.next_element.next_element.next_element.next_element.value = "e"
    my_name.next_element.next_element.next_element.next_element.next_element.value = "r"

def rename_to_anders():
    global my_name
    my_name.value = "A"
    my_name.next_element.value = "n"
    my_name.next_element.next_element.value = "d"
    time.sleep(0)
    my_name.next_element.next_element.next_element.value = "e"
    my_name.next_element.next_element.next_element.next_element.value = "r"
    my_name.next_element.next_element.next_element.next_element.next_element.value = "s"

def print_name_loop():
    global my_name
    while True:
        print(f"My name is {my_name}")
        time.sleep(0.1)

def update_name_loop():
    global my_name
    while True:
        rename_to_anders()
        rename_to_sander()

def example3():
    '''This example is also not protecting access to the resource it is using. Let's fix that'''

    thread1 = Thread(name="This thread is printing the name", target=print_name_loop)
    thread2 = Thread(name="And this one is updating it", target=update_name_loop)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
