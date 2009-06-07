import sys
import exceptions

class Scheduler:
  
  def __init__(self):
    pass
  
  '''
  schedule method should handle all jobs in the queue
  '''
  def schedule(self, queue):
    for job in queue.queued_jobs:
      if job.state == 'pending':
        
        try:
          probe = job.run()
          if probe != 'ok':
            print probe
            job.pending()
          else:
            job.complete()
        except:
          print probe
          job.pending()

class Queue:
  
  queued_jobs = []
  
  def __init__(self):
    self.queued_jobs = []
  
  '''
  add method should add a job to the queue
  '''
  def add(self, jobs):
    #print 'new jobs added to queue and set to pending: '
    for job in jobs:
      self.queued_jobs.append(job)
      job.pending()
  
  '''
  remove method should remove a job from the queue
  '''
  def remove(self, job):
    #print 'job removed from queue: ' + str(job)
    pass
  

class Job:
  
  state = ''
  task = object 
  
  def __init__(self, task):
    self.state = 'new'
    self.task = task
    #print 'new job object: ' + str(self) + ' with state: ' + str(self.state)
    
  def run(self):
    #print 'trying to run: ' + str(self)
    try:
      result = eval(self.task)
      print 'The result from task >> ' + str(self.task) + ' << is ' +  str(result)
      e = 'ok'
    except:
      e = sys.exc_info()[0]
      #print 'i cannot run: ' + str(self)
      #print 'cause: ', e
      #raise
    return e
  
  '''
  pending method should set a job's state property to pending
  '''
  def pending(self):
    self.state = 'pending'
    #print 'job is pending: ' + str(self)
  
  '''
  completed method should set the job's state property to completed
  '''
  def completed(self):
    self.state = 'completed'
    #print 'job completed: ' + str(self)

class Task:

  def __init__(self):
    pass

if __name__ == '__main__':
  
  s = Scheduler()
  
  task1 = '10 / 0'
  task2 = '100 * 5'
  
  j = Job(task1)
  j2 = Job(task2)
  
  q = Queue()
  
  q.add([ j, j2 ])
  
  s.schedule( q )










