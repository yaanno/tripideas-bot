import sys
import exceptions
import logging
from ..settings import SETTINGS
from .modules.messaging import Messaging

task_table = [
"""
messaging = Messaging()
messaging.collect_messages()
messaging.process_messages()
"""
]


class Scheduler:

  state = ''
  queue = object
  
  def __init__(self):
    self.state = 'init'
    self.log()
    self.fill_queue()
  
  '''
  The schedule method all jobs in the queue
  '''
  def schedule(self):
    for job in self.queue.queued_jobs:
      if job.state == 'pending':
        try:
          probe = job.run()
          if probe != 'ok':
            print probe
          else:
            queue.remove(job)
            job.complete()
        except:
          job.pending()

  def fill_queue(self):
    self.state = 'filling queue'
    self.log()
    
    self.queue = Queue()
    
    for task in task_table:
      job = Job(task)
      self.queue.add([ job ])
    
    self.state = 'filled'

  def log(self):
    pass
        
class Queue:
  
  queued_jobs = []
  state = ''
  
  def __init__(self):
    self.queued_jobs = []
    self.state = 'init'
    self.log()
  '''
  The add method adds a new job to the queue
  '''
  def add(self, jobs):
    for job in jobs:
      job.pending()
      self.queued_jobs.append(job)
      self.state = 'new job'
      self.log()
  
  '''
  The remove method removes a job from the queue
  '''
  def remove(self, job):
    self.queued_jobs.remove(job)
    
  def log(self):
    pass
    
class Job:
  
  state = ''
  task = object
  
  def __init__(self, task):
    self.state = 'new'
    self.task = task

  '''
  The run method executes arbitrary Python code (task) passed as argument
  '''
  def run(self):
    try:
      exec(self.task)
      e = 'ok'
    except:
      e = sys.exc_info()[0]
    return e
  
  '''
  pending method should set a job's state property to pending
  '''
  def pending(self):
    self.state = 'pending'
    self.log()
  
  '''
  completed method should set the job's state property to completed
  '''
  def completed(self):
    self.state = 'completed'
    self.log()

  def log(self):
    pass
    
__all__ = ["Job", "Queue", "Scheduler"]





