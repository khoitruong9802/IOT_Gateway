from typing import List, Dict
from design_pattern.observer import Observer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from scheduler.scheduler import Scheduler
from scheduler.task import TaskInfo
from datetime import datetime
from uuid import uuid4

class Loader(Observer):
  def __init__(self, scheduler: Scheduler) -> None:
    super().__init__()
    self.cron_job = BackgroundScheduler()
    self.cron_mapping: Dict[int, str] = {}
    self.cron_job.start()
    self.scheduler = scheduler
    
  def push_task_to_scheduler(self, task: TaskInfo) -> None:
    self.scheduler.add_task(task.generate_task())
    
  def update(self, data: List[TaskInfo] | int):
    if not isinstance(data, list):
      data = int(data)
      if data in self.cron_mapping:
        self.cron_job.remove_job(self.cron_mapping[data])
        del self.cron_mapping[data]
      return

    for task in data:
      try:
        date_time = task.start_time.split(":")
        hour, minute = int(date_time[0]), int(date_time[1])

        print(hour, minute)
        print(task.start_day, task.end_day)

        if task.id in self.cron_mapping:
          self.cron_job.remove_job(self.cron_mapping[task.id])
          del self.cron_mapping[task.id]

        if task.status == 0:
          continue

        cron_job_id = str(uuid4())
        self.cron_mapping[task.id] = cron_job_id

        # Check schedule type
        if task.schedule_type == "Daily":
          print("In daily")
          # Schedule daily
          self.cron_job.add_job(
            self.push_task_to_scheduler,
            CronTrigger(
              hour=hour,
              minute=minute,
              start_date=task.start_day,
              end_date=task.end_day
            ),
            args=(task,),
            id=cron_job_id
          )

        elif task.schedule_type == "Weekly":
          print("In weekly")
          # Ensure task.days is provided for weekly schedules
          if task.days:
            days_of_week = ",".join(str(day - 2) for day in task.days)  # APScheduler expects string
            self.cron_job.add_job(
              self.push_task_to_scheduler,
              CronTrigger(
                day_of_week=days_of_week,
                hour=hour,
                minute=minute,
                start_date=task.start_day,
                end_date=task.end_day
              ),
              args=(task,),
              id=cron_job_id
            )
          else:
            print(f"Task {task.id} has no 'days' specified for weekly schedule.")

        elif task.schedule_type == "Once":
          print("In once")
          task_datetime = datetime.strptime(
            f"{task.start_day} {task.start_time}",
            "%Y-%m-%d %H:%M"
          )
          self.cron_job.add_job(
            self.push_task_to_scheduler,
            DateTrigger(run_date=task_datetime),  # Use DateTrigger for a one-time job
            args=(task,),
            id=cron_job_id
          )

      except ValueError:
        print(f"Invalid start_time format for task: {task.id}")
    
  