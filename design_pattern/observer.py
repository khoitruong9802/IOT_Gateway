from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
  @abstractmethod
  def update(self, data):
    pass

class Subject:
  def __init__(self) -> None:
    self.observers: List[Observer] = []

  def add_observer(self, observer: Observer) -> None:
    self.observers.append(observer)

  def remove_observer(self, observer: Observer) -> bool:
    try:
      self.observers.remove(observer)
      return True
    except:
      return False
    
  def send_notify(self, data):
    for observer in self.observers:
      observer.update(data)