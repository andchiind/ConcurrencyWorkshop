from __future__ import annotations

from dataclasses import dataclass
from queue import Empty, Queue
from threading import Thread
from typing import Callable, Generic, List, Optional, TypeVar

from enum import Enum


T = TypeVar('T')
T1 = TypeVar('T1')

type Job = Callable[[Queue, Queue], None]
type Task = Callable[[Queue, Queue], None]
type Action = Callable[[T], T1]

class StageType(Enum):
    PIPE = 1
    Map = 2
    WORKER = 3
    REDUCE = 4

@dataclass
class PipeStruct(Generic[T, T1]):
    stages: List[Stage]

@dataclass
class MapStruct(Generic[T, T1]):
    stage: Stage
    n_workers: int

@dataclass
class Stage(Generic[T, T1]):
    type: StageType
    worker: Optional[WorkerStruct[T, T1]] = None
    pipeline: Optional[PipeStruct[T, T1]] = None
    map: Optional[MapStruct[T, T1]] = None
    reduce: Optional[ReduceStruct[T, T1]] = None

@dataclass
class WorkerStruct(Generic[T, T1]):
    func: Callable[[T], T1]

@dataclass
class ReduceStruct(Generic[T, T1]):
    func: Callable[[T, T], T1]
    n_workers: int

def run_worker(input_queue: Queue[T], output_queue: Queue[T1], worker: WorkerStruct[T, T1]):
    while not input_queue.empty():
        try:
            task = input_queue.get_nowait()
            result = worker.func(task)
            output_queue.put(result, timeout=10) # Currently no error handling here
        except Empty:
            continue
    return output_queue

def run_reduce_worker(input_queue: Queue[T], reducer: ReduceStruct[T, T1]):
    while input_queue.qsize() > 1:
        try:
            task1 = input_queue.get()
            task2 = input_queue.get()
            result = reducer.func(task1, task2)
            input_queue.put(result) # Currently no error handling here
        except Empty:
            continue
    return input_queue

def run_reduce(input_queue: Queue[T], output_queue: Queue[T1], reducer: ReduceStruct[T, T1]):
    threads: List[Thread] = []
    for _ in range(reducer.n_workers):
        thread = Thread(target=run_reduce_worker, args=(input_queue, reducer))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    output = input_queue.get()
    output_queue.put(output)
    return output_queue

def run_map(input_queue: Queue[T], output_queue: Queue[T1], map: MapStruct[T, T1]):
    map_workers: List[Thread] = []
    for _ in range(map.n_workers):
        thread = Thread(target=run_stage, args=(input_queue, output_queue, map.stage))
        thread.start()
        map_workers.append(thread)
    for map_worker in map_workers:
        map_worker.join()
    return output_queue

def run_pipeline(input_queue: Queue[T], output_queue: Queue[T1], pipeline: PipeStruct[T, T1]):
    pipeline_workers: List[Thread] = []
    current_input_queue = input_queue
    for i in range(len(pipeline.stages)):
        current_output_queue = Queue() if i < len(pipeline.stages) - 1 else output_queue
        current_stage: Stage = pipeline.stages[i]
        thread = Thread(target=run_stage, args=(current_input_queue, current_output_queue, current_stage))
        thread.start()
        pipeline_workers.append(thread)
        current_input_queue = current_output_queue
    for pipeline_worker in pipeline_workers:
        pipeline_worker.join()
    return output_queue

def run_stage(input_queue: Queue, output_queue: Queue, stage: Stage):
    if stage.type == StageType.WORKER:
        output_queue = run_worker(input_queue, output_queue, stage.worker)
    elif stage.type == StageType.PIPE:
        output_queue = run_pipeline(input_queue, output_queue, stage.pipeline)
    elif stage.type == StageType.Map:
        output_queue = run_map(input_queue, output_queue, stage.map)
    elif stage.type == StageType.REDUCE:
        output_queue = run_reduce(input_queue, output_queue, stage.reduce)
    return output_queue

def Worker(func: Callable) -> Stage:
    return Stage(type=StageType.WORKER, worker=WorkerStruct(func=func))

def Map(stage: Stage, n_workers: int) -> Stage:
    return Stage(type=StageType.Map, map=MapStruct(stage=stage, n_workers=n_workers))

def Pipe(stages: List[Stage]) -> Stage:
    return Stage(type=StageType.PIPE, pipeline=PipeStruct(stages=stages))

def Reduce(func: Callable[[T, T], T1], n_workers: int) -> Stage:
    return Stage(type=StageType.REDUCE, reduce=ReduceStruct(func=func, n_workers=n_workers))

def example_computation():
    workers_n = 4
    input_queue = Queue()
    fibonacci_range = 40

    for i in range(fibonacci_range):
        input_queue.put(i)

    # TODO: we want to do the following:
    # - calculate the fibonacci value for each item in the input
    # - calculate if the output is a prime number
    # - calculate the total number of prime numbers
    # In other words: calculate the number of prime fibonacci numbers from 0 to 'fibonacci_range'

def add(a: int, b: int):
    return a + b

def fib(n: int) -> int:
    if n == 0: return 0
    a = 0
    b = 1
    next = b
    for _ in range(1, n - 1):
        a, b = b, next
        next = a + b
    return next

def is_prime(n: int) -> bool:
    if n <= 1: return False

    for i in range(2, n):
        if n % i == 0: return False
    return True

def bool_to_int(bool_expr: bool) -> int:
    return 1 if bool_expr else 0
