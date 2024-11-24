from scheduler.task import TaskPCB
from enum import Enum
from time import sleep
from utilities.rs485 import Fertilizer

class CoreState(Enum):
  RUNNING = 1
  IDLE = 2

class Core:
  def __init__(self, core_id: str):
    self.core_id = core_id
    self.core_state: CoreState = CoreState.IDLE

  def run(self, task_PCB: TaskPCB) -> TaskPCB | None:
    self.core_state = CoreState.RUNNING
  
    program_pointer = task_PCB.program_pointer
 
    instruction = task_PCB.instructions[program_pointer]
    task_PCB.program_pointer += 1
  
    if instruction.get("instr") == "watering":
      # fertilizer = Fertilizer()
      flow = instruction.get("args").split(" ")
      print("relay 1 on")
      # fertilizer.control_relay(1, True)
      print("relay 2 on")
      # fertilizer.control_relay(2, True)
      print("relay 3 on")
      # fertilizer.control_relay(3, True)
   
      print(f"flow 1 = {flow[0]}")
      print(f"flow 2 = {flow[1]}")
      print(f"flow 3 = {flow[2]}")
      sleep(max(int(flow[0]), int(flow[1]), int(flow[2])) / 5)
   
      print("relay 1 off")
      # fertilizer.control_relay(1, False)
      print("relay 2 off")
      # fertilizer.control_relay(2, False)
      print("relay 3 off")
      # fertilizer.control_relay(3, False)
      print("end!!!!!!!!")


    self.core_state = CoreState.IDLE
    if task_PCB.program_pointer >= task_PCB.program_size:
      return None
    return task_PCB