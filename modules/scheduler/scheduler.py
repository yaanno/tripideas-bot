import sys
import exceptions

class Scheduler:
  
  def __init__(self):
    pass
  
  '''
  The schedule method all jobs in the queue
  '''
  def schedule(self, queue):
    for job in queue.queued_jobs:
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

class Queue:
  
  queued_jobs = []
  
  def __init__(self):
    self.queued_jobs = []
  
  '''
  The add method adds a new job to the queue
  '''
  def add(self, jobs):
    for job in jobs:
      job.pending()
      self.queued_jobs.append(job)
  
  '''
  The remove method removes a job from the queue
  '''
  def remove(self, job):
    self.queued_jobs.remove(job)
  

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
      print self.task.code
      result = eval(self.task.code)
      e = 'ok'
    except:
      e = sys.exc_info()[0]
    return e
  
  '''
  pending method should set a job's state property to pending
  '''
  def pending(self):
    self.state = 'pending'
  
  '''
  completed method should set the job's state property to completed
  '''
  def completed(self):
    self.state = 'completed'

class Task:
  
  code = object

  def __init__(self, code):
    self.code = code
