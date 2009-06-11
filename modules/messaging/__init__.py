import os
import re
from settings import *
from modules import twitter as tw
from string import replace
from models import *
import logging

twitter = tw.Twitter(
  SETTINGS['Tripideas']['username'], 
  SETTINGS['Tripideas']['password'], 
  format=SETTINGS['Tripideas']['format']
)

class Messaging:

  messages = {}
  mentions = {}

  def __init__(self):
    self.messages = {}
    self.mentions = {}
  
  def collect_messages(self):
    ''' Collect all messages that mentions us '''
    self.messages = twitter.statuses.mentions()
    
  def save_message(self):
    pass
    
  def process_messages(self):
  
    if len(self.messages) > 0:
      counter = 0
      
      self.mentions = {'messages':{}}
      
      for message in self.messages:
      
        msg = self.test_expression(message, '#flight')
        if msg is not False:
          text = message['text']
          message = re.split(' ', str(text))
          
          cat = message[1]
          dest = re.split('-', message[2])
          fr = dest[0]
          to = dest[1]
          
          pattern = re.compile('(\d{4})-(\d{2})-(\d{2})')
          dates = pattern.findall(message[3])
          dep = { 'year' : dates[0][0], 'month' : dates[0][1], 'day' : dates[0][2] }
          ret = { 'year' : dates[1][0], 'month' : dates[1][1], 'day' : dates[1][2] }
          
          self.mentions = {'type' : cat, 'from' : fr, 'to' : to, 'departure' : dep, 'retour' : ret }
          

  def test_expression(self, message, expr):
    
    msg = re.search(expr, str(message))

    logging.debug(msg)
    
    if msg is not None:
        return True
    else:
      return False
  
  def get_message(self):
    pass
    
  def fake(self):
    mentions = {'messages':{}}
    counter = 0
    for message in messages:
      msg = re.search('#ping', str(message))
      if msg is not None:
        msgout = msg.group(0)
        if msgout is not None:
          mentions['messages'][('%s' % counter)] = message
          counter += 1
  
  
  
  def handle_messages(self):

    a = Author(
      author_id = message['user']['id'],
      protected = message['user']['protected'],
      name = message['user']['name'],
      screen_name = message['user']['screen_name'],
    )
    a.put()

    m = Message(
      body = message['text'],
      message_id = message['id'],
      reply_id = message['in_reply_to_user_id'],
      author = a
    )
    m.put()
    
