from typing import List
from design_pattern.observer import Observer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scheduler.scheduler import Scheduler
from scheduler.task import TaskInfo

class Loader(Observer):
  def __init__(self, scheduler: Scheduler) -> None:
    super().__init__()
    self.cron_job = BackgroundScheduler()
    self.scheduler = scheduler
    self.cron_job.start()
    
  def push_task_to_scheduler(self, task: TaskInfo) -> None:
    self.scheduler.add_task(task.generate_task())
    
  def update(self, data: List[TaskInfo]):
    for task in data:
      date_time = task.start_time.split(":")
      self.cron_job.add_job(self.push_task_to_scheduler, CronTrigger(hour=int(date_time[0]), minute=int(date_time[1])), args=(task, ))
    
  