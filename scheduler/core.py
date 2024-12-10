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

  def run(self, task_PCB: TaskPCB) -> TaskPCB:
    self.core_state = CoreState.RUNNING
  
    program_pointer = task_PCB.program_pointer
 
    instruction = task_PCB.instructions[program_pointer]
    task_PCB.program_pointer += 1
  
    if instruction.get("instr") == "watering":
      watering_args = instruction.get("args").split(" ")

      # fertilizer = Fertilizer()
      # fertilizer.control_relay(1, True)
      # sleep(int(watering_args[0]) / 5)
      # fertilizer.control_relay(1, False)

      # fertilizer.control_relay(2, True)
      # sleep(int(watering_args[1]) / 5)
      # fertilizer.control_relay(2, False)

      # fertilizer.control_relay(3, True)
      # sleep(int(watering_args[2]) / 5)
      # fertilizer.control_relay(3, False)

      # fertilizer.control_relay(7, True)
      # sleep(5)
      # fertilizer.control_relay(7, False)

      # fertilizer.control_relay(int(watering_args[3]) + 3, True)
      # sleep(0.5)

      # fertilizer.control_relay(8, True)
      # sleep(5)
      # fertilizer.control_relay(8, False)

      # sleep(0.5)
      # fertilizer.control_relay(int(watering_args[3]) + 3, False)

      print(f"flow 1 = {watering_args[0]}")
      print("Relay 1 on")
      sleep(int(watering_args[0]) / 5)
      print("Relay 1 off")

      print(f"flow 2 = {watering_args[1]}")
      print("Relay 2 on")
      sleep(int(watering_args[1]) / 5)
      print("Relay 2 off")

      print(f"flow 3 = {watering_args[2]}")
      print("Relay 3 on")
      sleep(int(watering_args[2]) / 5)
      print("Relay 3 off")

      print("Pump in")
      print("Relay 7 on")
      sleep(5)
      print("Relay 7 off")

      print(f"Open water valve area {int(watering_args[3]) + 3}")
      print(f"Relay {int(watering_args[3]) + 3} on")
      sleep(0.5)

      print("Pump out")
      print("Relay 8 on")
      sleep(5)
      print("Relay 8 off")

      print(f"Close water valve area {int(watering_args[3]) + 3}")
      print(f"Relay {int(watering_args[3]) + 3} off")
      sleep(0.5)
   
      print("end!!!!!!!!")

    self.core_state = CoreState.IDLE
    return task_PCB