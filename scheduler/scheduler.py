from abc import ABC, abstractmethod
from scheduler.task import TaskPCB
from typing import List
import heapq
                    
class Scheduler(ABC):
  @abstractmethod
  def add_task(self, task_PCB: TaskPCB):
    pass

  @abstractmethod
  def get_task(self) -> TaskPCB:
    pass

  @abstractmethod
  def is_empty(self) -> bool:
    pass
  
class SchedulerFactory:
  @staticmethod
  def get_scheduler(scheduler_algorithm: str) -> Scheduler:
    if scheduler_algorithm == "FCFS":
      return FCFS()
    elif scheduler_algorithm == "RoundRobin":
      return RoundRobin()
    elif scheduler_algorithm == "Preemptive":
      return Preemptive()

class FCFS(Scheduler):
  def __init__(self):
    self.ready_queue: List[TaskPCB] = []
  
  def add_task(self, task_PCB: TaskPCB):
    self.ready_queue.append(task_PCB)

  def get_task(self) -> TaskPCB | None:
    if (self.is_empty()):
      return None
    return self.ready_queue.pop()

  def is_empty(self) -> bool:
    return len(self.ready_queue) == 0

class RoundRobin(Scheduler):
  def __init__(self):
    self.ready_queue: List[TaskPCB] = []

  def add_task(self, task_PCB: TaskPCB):
    self.ready_queue.insert(0, task_PCB)

  def get_task(self) -> TaskPCB | None:
    if (self.is_empty()):
      return None
    return self.ready_queue.pop()

  def is_empty(self) -> bool:
    return len(self.ready_queue) == 0

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        # Invert the priority to simulate a max-heap
        heapq.heappush(self.heap, (-priority, item))

    def pop(self):
        # Invert the priority back to get the original priority
        return heapq.heappop(self.heap)[1]

    def is_empty(self):
        return len(self.heap) == 0

class Preemptive(Scheduler):
  def __init__(self):
    self.ready_queue = PriorityQueue()

  def add_task(self, task_PCB: TaskPCB):
    self.ready_queue.push(task_PCB, task_PCB.priority)

  def get_task(self) -> TaskPCB | None:
    if (self.is_empty()):
      return None
    return self.ready_queue.pop()

  def is_empty(self) -> bool:
    return self.ready_queue.is_empty()