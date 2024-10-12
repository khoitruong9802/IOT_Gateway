import json
from typing import List, Dict
from design_pattern.observer import Observer
from design_pattern.observer import Subject
from scheduler.task import TaskInfo

class Store(Observer, Subject):
  def __init__(self, file_name) -> None:
    super().__init__()
    self.data: List[TaskInfo] = []
    self.file_name = file_name

  def load_data(self) -> None:
    with open(self.file_name, "r", encoding="utf-8") as file:
      json_data = json.load(file)
      self.data = [TaskInfo(item) for item in json_data]
      self.send_notify(self.data)

  def get_data(self) -> List[TaskInfo]:
    return self.data
  
  def get_data_dict(self) -> Dict:
    return [item.to_dict() for item in self.data]
  
  def set_data(self, data: List[TaskInfo]) -> None:
    self.data = data
    with open(self.file_name, "w", encoding="utf-8") as file:
      json.dump(self.get_data_dict(), file, ensure_ascii=False, indent=2)
      
  def append_item(self, data: TaskInfo) -> None:
    self.data.append(data)
    with open(self.file_name, "w", encoding="utf-8") as file:
      json.dump(self.get_data_dict(), file, ensure_ascii=False, indent=2)
      
  def remove_item(self, id: int) -> None:
    self.data = [item for item in self.data if item.id != id]
    with open(self.file_name, "w", encoding="utf-8") as file:
      json.dump(self.get_data_dict(), file, ensure_ascii=False, indent=2)
      
  def update(self, data):
    feed_id = data[0]
    payload = data[1]

    if (feed_id == "schedules"):
      schedule_dict = json.loads(payload)
      schedule: TaskInfo = TaskInfo(schedule_dict)
      
      if (schedule_dict["method"] == "ADD"):
        self.append_item(schedule)
        self.send_notify([schedule, ])

      elif (schedule_dict["method"] == "DEL"):
        self.remove_item(schedule.id)

      elif (schedule_dict["method"] == "UPDATE"):
        pass
