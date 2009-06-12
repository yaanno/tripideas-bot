from ..settings import SETTINGS
from .modules.scheduler import Scheduler
import logging

class Cron:

  state = ''
  scheduler = object
  
  def __init__(self):
    self.state = 'init'
    self.log()
    
  def run(self):
    self.state = 'running'
    self.log()
    if self.scheduler.state == 'filled':
      self.scheduler.schedule()
    
  def stop(self):
    self.state = 'stopped'
    self.log()
  
  def init_scheduler(self):
    self.scheduler = Scheduler()
  
  def log(self):
    pass
  
__all__ = ["Cron"]