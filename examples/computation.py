from __future__ import annotations

from dataclasses import dataclass
from queue import Queue
from typing import Callable, Generic, List, Optional, TypeVar

from enum import Enum

Tinput = TypeVar('Tinput')
Toutput = TypeVar('Toutput')

type Job = Callable[[Queue, Queue], None]
type Task = Callable[[Queue, Queue], None]
type Action = Callable[[Tinput], Toutput]

class NodeType(Enum):
    PIPE = 1
    Map = 2
    WORKER = 3
    REDUCE = 4

@dataclass
class PipeStruct(Generic[Tinput, Toutput]):
    nodes: List[Node]

@dataclass
class MapStruct(Generic[Tinput, Toutput]):
    node: Node
    n_workers: int

@dataclass
class Node(Generic[Tinput, Toutput]):
    type: NodeType
    worker: Optional[WorkerStruct[Tinput, Toutput]] = None
    pipeline: Optional[PipeStruct[Tinput, Toutput]] = None
    map: Optional[MapStruct[Tinput, Toutput]] = None
    reduce: Optional[ReduceStruct[Tinput, Toutput]] = None

@dataclass
class WorkerStruct(Generic[Tinput, Toutput]):
    func: Callable[[Tinput], Toutput]

@dataclass
class ReduceStruct(Generic[Tinput, Toutput]):
    func: Callable[[Tinput, Tinput], Toutput]
    n_workers: int

def Worker(func: Callable) -> Node:
    return Node(type=NodeType.WORKER, worker=WorkerStruct(func=func))

def Map(node: Node, n_workers: int) -> Node:
    return Node(type=NodeType.Map, map=MapStruct(node=node, n_workers=n_workers))

def Pipe(nodes: List[Node]) -> Node:
    return Node(type=NodeType.PIPE, pipeline=PipeStruct(nodes=nodes))

def Reduce(func: Callable[[Tinput, Tinput], Toutput], n_workers: int) -> Node:
    return Node(type=NodeType.REDUCE, reduce=ReduceStruct(func=func, n_workers=n_workers))

def get_input_data(length: int) -> Queue[int]:
    input_queue: Queue[int] = Queue()
    for i in range(length):
        input_queue.put(i)
    return input_queue

def example_computation():
    n = 10
    input_queue = get_input_data(n)

    # TODO: we want to do the following:
    # - calculate the fibonacci value for each item in the input
    # - calculate if the output is a prime number
    # - calculate the total number of prime numbers
    # In other words: calculate the number of prime fibonacci numbers from 0 to 'n'

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
