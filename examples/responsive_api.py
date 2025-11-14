from random import random
from threading import Thread
import time

train_stopping = False

class TrainDriver(Thread):
    def __init__(self):
        Thread.__init__(self, name="Train driver")

    def run(self):
        global train_stopping
        while True:
            # TODO: decide whether to start or stop the train
            raise NotImplementedError()

class TrainCoordinator(Thread):
    def __init__(
        self
    ):
        Thread.__init__(self, name="Train coordinator thread")

    def run(self) -> None:
        while True:
            # TODO: get telemetry values
            # TODO: make the telemetry data available in a useful way to the API
            # TODO: communicate with the TrainDriver on behalf of the API

            # We can assume the following calculation for speed: power_estimate * (1 - gradient_estimate)
            raise NotImplementedError()

def gradient_telemetry():
    global train_stopping
    current_gradient = 0.0
    while True:
        time.sleep(0.25)
        if train_stopping:
            continue
        if random() > 0.8:
            current_gradient = max(current_gradient - 0.02, 0.0)
        else:
            current_gradient = min(current_gradient + 0.02, 0.7)

def engine_power_telemetry():
    global train_stopping
    current_power = 0.0
    while True:
        time.sleep(0.25)
        if train_stopping:
            current_power = max(current_power - 5.0, 0.0)
        elif random() > 0.5:
            current_power = max(current_power - 5.0, 100.0)
        else:
            current_power = min(current_power + 5.0, 1000.0)

def API():
    while True:
        user_request = input("SPEED to get current SPEED, STOP to stop and START to start\n")
        if user_request == "SPEED":
            raise NotImplementedError()
        elif user_request == "STOP":
            raise NotImplementedError()
        elif user_request == "START":
            raise NotImplementedError()


def responsive_api():
    engine_power_telemetry_thread = Thread(name="Even numbers", target=engine_power_telemetry)
    track_gradient_telemetry_thread = Thread(name="Odd numbers", target=gradient_telemetry)

    mock_train_driver = TrainDriver()
    mock_train_driver.start()

    coordinator = TrainCoordinator()
    coordinator.start()

    print()

    number_of_api_threads = 1
    api_threads = []
    for i in range(number_of_api_threads):
        api_thread = Thread(name=f"API thread {i}", target=API)
        api_thread.start()
        api_threads.append(api_thread)

    engine_power_telemetry_thread.start()
    track_gradient_telemetry_thread.start()
    coordinator.join() # Keeps the main thread alive
