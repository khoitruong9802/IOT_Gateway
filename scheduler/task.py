from typing import Dict, List
from typing import TypedDict

class Instruction(TypedDict):
  instr: str
  args: str

class TaskPCB:
	def __init__(self, priority: int, instructions: List[Instruction], program_size: int) -> None:
		self.prioty: int = priority
		self.instructions: List[Instruction] = instructions
		self.program_pointer: int = 0
		self.program_size: int = program_size

class TaskInfo:
	def __init__(self, data: Dict):
		self.id: int = data.get("id")
		self.schedule_name: str = data.get("schedule_name")
		self.priority: int = data.get("priority")
		self.description: str = data.get("description")
		self.start_time: str = data.get("start_time")
		self.stop_time: str = data.get("stop_time")
		self.flow1: int = data.get("flow1")
		self.flow2: int = data.get("flow2")
		self.flow3: int = data.get("flow3")
		self.cycle: int = data.get("cycle")
		self.area: int = data.get("area")
		self.everyday: bool = data.get("everyday")
		self.date: str = data.get("date")

	def to_dict(self) -> Dict:
		return self.__dict__

	def generate_task(self) -> TaskPCB:
		instructions = [{
			"instr": "watering",
			"args": f"{self.flow1} {self.flow2} {self.flow3}"
		} for i in range(self.cycle)]
		return TaskPCB(self.priority, instructions, self.cycle)