from typing import Dict, List
from typing import TypedDict
from uuid import uuid4

class Instruction(TypedDict):
  instr: str
  args: str

class TaskPCB:
  def __init__(self, schedule_id: int, schedule_name: str, priority: int, instructions: List[Instruction], program_size: int) -> None:
    self.task_id: str = str(uuid4())
    self.task_start_time: str = ""
    self.task_end_time: str = ""
    self.schedule_id: int = schedule_id
    self.schedule_name: int = schedule_name
    self.priority: int = priority
    self.instructions: List[Instruction] = instructions
    self.program_pointer: int = 0
    self.program_size: int = program_size

  def __lt__(self, other):
    return self.priority < other.priority

  def __eq__(self, other):
    return self.priority == other.priority
  
  def __gt__(self, other):
    return self.priority > other.priority


class TaskInfo:
  def __init__(self, data: Dict):
    self.id: int = data.get("id")
    self.schedule_name: str = data.get("schedule_name")
    self.priority: int = data.get("priority")
    self.area: int = data.get("area")
    self.description: str = data.get("description")
    self.flow1: int = data.get("flow1")
    self.flow2: int = data.get("flow2")
    self.flow3: int = data.get("flow3")
    self.cycle: int = 0
    self.status: int = data.get("status")
    self.start_time: str = data.get("start_time")
    self.stop_time: str = data.get("stop_time")
    self.schedule_type: bool = data.get("schedule_type")
    self.start_day: str = data.get("start_day")
    self.end_day: str = data.get("end_day")
    self.fertilizer_device_id: int = 1
    self.days: List[int] = data.get("days")

  def to_dict(self) -> Dict:
    return self.__dict__

  def generate_task(self) -> TaskPCB:
    total_flow = self.flow1 + self.flow2 + self.flow3
    cycle = total_flow // 3
    temp = cycle * 3
    new_flow1 = self.flow1 * temp / total_flow / cycle
    new_flow2 = self.flow2 * temp / total_flow / cycle
    new_flow3 = self.flow3 * temp / total_flow / cycle

    instructions = [{
      "instr": "watering",
      "args": f"{new_flow1} {new_flow2} {new_flow3} {self.area}"
    } for i in range(cycle)]

    if total_flow % 3 != 0:
      instructions.append({
        "instr": "watering",
        "args": f"{self.flow1 - new_flow1 * cycle} {self.flow2 - new_flow2 * cycle} {self.flow3 - new_flow3 * cycle} {self.area}"
      })
    self.cycle = cycle if total_flow % 3 == 0 else cycle + 1
    return TaskPCB(self.id, self.schedule_name, self.priority, instructions, self.cycle)