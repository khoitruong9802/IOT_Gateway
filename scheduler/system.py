from utilities.mqtt_broker import MQTTBroker
from typing import Literal
from scheduler.store import Store
from scheduler.scheduler import SchedulerFactory
from scheduler.loader import Loader
from scheduler.core import Core
from threading import Thread
from datetime import datetime
from scheduler.control_relay import ControlRelay
import json

import time
  
class System:
  def __init__(self, mqtt_broker: MQTTBroker, store: str, algorithm: Literal["FCFS", "RoundRobin", "Preemptive"]) -> None:
    """
    Represents a system that interacts with an MQTT broker and uses a specified scheduling algorithm.

    This class is responsible for managing communication with the given MQTT broker and implementing
    a scheduling algorithm to handle tasks. The supported algorithms are "FCFS" (First-Come, First-Served),
    "RoundRobin", and "Preemptive".

    Attributes:
      mqtt_broker (MQTTBroker): The MQTT broker used for communication.
      store (str): The storage location or identifier where data or tasks are saved.
      algorithm (Literal["FCFS", "RoundRobin", "Preemptive"]): The scheduling algorithm used for task processing.
        - "FCFS": Tasks are processed in the order they are received.
        - "RoundRobin": Tasks are processed in a cyclic manner with time slices.
        - "Preemptive": Tasks are prioritized, and higher-priority tasks can interrupt or preempt lower-priority tasks.

    Args:
      mqtt_broker (MQTTBroker): The MQTT broker for sending and receiving messages.
      store (str): The name or path of the storage system (relative path).
      algorithm (Literal["FCFS", "RoundRobin", "Preemptive"]): The scheduling algorithm to be used, either "FCFS", "RoundRobin", or "Preemptive".

    Example:
      >>> system = System(mqtt_broker=my_broker, store="task_store.json", algorithm="FCFS")
    """
    self.mqtt_client = mqtt_broker
    self.store = Store(store)
    self.scheduler = SchedulerFactory.get_scheduler(algorithm)
    self.loader = Loader(self.scheduler)
    self.control_relay = ControlRelay()
    self.core = Core("core")

    self.mqtt_client.add_observer(self.store)
    self.mqtt_client.add_observer(self.control_relay)
    self.store.add_observer(self.loader)
    self.store.load_data()
  
  def _run(self) -> None:
    while True:
      if self.scheduler.is_empty():
        continue
      else:
        task_PCB = self.scheduler.get_task()

        if task_PCB.program_pointer == 0:
          current_datetime = datetime.now()
          formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
          task_PCB.task_start_time = formatted_datetime
          
          message = {
            "task_id": task_PCB.task_id,
            "schedule_id": task_PCB.schedule_id,
            "timestamp": formatted_datetime,
            "message_type": "schedule_begin",
            "message": f"({formatted_datetime}) {task_PCB.schedule_name} has started operating"
          }
          self.mqtt_client.publish("gateway-send", json.dumps(message, separators=(',', ':')), 1)

        task_PCB = self.core.run(task_PCB)

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        if task_PCB.program_pointer >= task_PCB.program_size:
          task_PCB.task_end_time = formatted_datetime

          message = {
            "task_id": task_PCB.task_id,
            "schedule_id": task_PCB.schedule_id,
            "timestamp": formatted_datetime,
            "message_type": "schedule_end",
            "message": f"({formatted_datetime}) {task_PCB.schedule_name} has been completed",
            "task_start_time": task_PCB.task_start_time,
            "task_end_time": task_PCB.task_end_time
          }
        else:
          message = {
            "task_id": task_PCB.task_id,
            "schedule_id": task_PCB.schedule_id,
            "timestamp": formatted_datetime,
            "message_type": "schedule_progress",
            "message": f"({formatted_datetime}) {task_PCB.schedule_name} is {(task_PCB.program_pointer / task_PCB.program_size * 100):.1f}% complete"
          }
          self.scheduler.add_task(task_PCB)

        self.mqtt_client.publish("gateway-send", json.dumps(message, separators=(',', ':')), 1)

      time.sleep(1)
      
  def run_background(self):
    """Starts a background thread to run this system"""
    thread = Thread(target=self._run, args=())
    thread.daemon = True
    thread.start()
    
  def run_blocking(self):
    """This call will block execution of your program and will not return"""
    self._run()