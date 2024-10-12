from utilities.adafruit_mqtt import AdafruitMQTT
from typing import Literal
from scheduler.store import Store
from scheduler.scheduler import SchedulerFactory
from scheduler.loader import Loader
from scheduler.core import Core
from threading import Thread

import time
  
class System:
  def __init__(self, mqtt_broker: AdafruitMQTT, store: str, algorithm: Literal["FCFS", "RoundRobin"]) -> None:
    """
    Represents a system that interacts with an MQTT broker and uses a specified scheduling algorithm.

    This class is responsible for managing communication with the given MQTT broker and implementing
    a scheduling algorithm to handle tasks. The supported algorithms are "FCFS" (First-Come, First-Served)
    and "RoundRobin".

    Attributes:
      mqtt_broker (AdafruitMQTT): The MQTT broker used for communication.
      store (str): The storage location or identifier where data or tasks are saved.
      algorithm (Literal["FCFS", "RoundRobin"]): The scheduling algorithm used for task processing.
        - "FCFS": Tasks are processed in the order they are received.
        - "RoundRobin": Tasks are processed in a cyclic manner with time slices.

    Args:
      mqtt_broker (AdafruitMQTT): The MQTT broker for sending and receiving messages.
      store (str): The name or path of the storage system (relative path).
      algorithm (Literal["FCFS", "RoundRobin"]): The scheduling algorithm to be used, either "FCFS" or "RoundRobin".

    Example:
      >>> system = System(mqtt_broker=my_broker, store="task_store.json", algorithm="FCFS")
    """
    self.ada = mqtt_broker
    self.store = Store(store)
    self.scheduler = SchedulerFactory.get_scheduler(algorithm)
    self.loader = Loader(self.scheduler)
    self.core1 = Core("core 1")
    self.ada.add_observer(self.store)
    self.store.add_observer(self.loader)
    self.store.load_data()
  
  def _run(self) -> None:
    while True:
      if self.scheduler.is_empty():
        continue
      else:
        task_PCB = self.scheduler.get_task()
        task_PCB = self.core1.run(task_PCB)
        if (task_PCB != None):
          self.scheduler.add_task(task_PCB)
          
      time.sleep(1)
      
  def run_background(self):
    """Starts a background thread to run this system"""
    thread = Thread(target=self._run, args=())
    thread.daemon = True
    thread.start()
    
  def run_blocking(self):
    """This call will block execution of your program and will not return"""
    self._run()