import os
import re
import logging
import time
from settings import *
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from modules.xml2dict import *
from modules import twitter as tw
from modules import kayak
from modules import simplejson as j

from string import replace

from models import *

twitter = tw.Twitter(
  SETTINGS['Tripideas']['username'], 
  SETTINGS['Tripideas']['password'], 
  format=SETTINGS['Tripideas']['format']
)

kayak = kayak.Kayak(
  SETTINGS['Kayak']['API_TOKEN'],
  SETTINGS['Kayak']['BASE_URL'],
)

class MainHandler(webapp.RequestHandler):
  def get(self):
    messages = twitter.statuses.mentions()
    mydict = {'messages':{}}
    counter = 0
    for message in messages:
      mydict['messages'][('%s' % counter)] = message
      counter += 1
      
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, mydict))

class CronHandler(webapp.RequestHandler):
  def get(self):
    pass
    

class KayakApi(webapp.RequestHandler):

  def get(self):
    
    kayak_session = kayak.get_session()
    logging.debug(kayak_session.content)
    
    session_id = re.search('<sid>(.*?)</sid>', kayak_session.content)
    session_id = session_id.group(1)
    
    kayak.session_id = session_id
    kayak.headers = { 'Cookie' : kayak_session.headers['set-cookie'] }
    
    kayak_search = kayak.post_search()
    logging.debug(kayak_search.content)
    
    search_id = re.search('<searchid>(.*?)</searchid>', kayak_search.content)
    search_id = search_id.group(1)
    
    kayak.search_id = search_id
    kayak_results = kayak.get_results()
    logging.debug(kayak_results.content)

    result_set = ''

    more_pending = re.search('<morepending>true</morepending>', kayak_results.content)
    
    if more_pending.group(0) is not None:
      more_pending = True
    
    if more_pending:
      time.sleep(10)
      kayak_results = kayak.get_results()
      result_set = kayak_results.content
      logging.debug(kayak_results.content)
      
    content = replace(result_set, '&', '&amp;')
    xml = XML2Dict()
    trips = xml.fromstring(content)
    trip_dict = {'trips' : trips}
    path = os.path.join(os.path.dirname(__file__), 'templates/kayak.html')
    self.response.out.write(template.render(path, trip_dict))

class KayakHandler(webapp.RequestHandler):
  
  def get(self):
    file = open('kayak-result.xml','r')
    content = file.read()
    content = replace(content, '&', '&amp;')
    xml = XML2Dict()
    trips = xml.fromstring(content)
    trip_dict = {'trips' : trips}
    '''
    xml = ET.fromstring(content)
    trips = xml.findall("trips/trip")
    trip_dict = {'trips' : trips}
    '''
    path = os.path.join(os.path.dirname(__file__), 'templates/kayak.html')
    self.response.out.write(template.render(path, trip_dict))
    
class ClearTripHandler(webapp.RequestHandler):
  
  def get(self):
    file = open('result.xml','r')
    content = file.read()
    content = replace(content, '&', '&amp;')
    xml = XML2Dict()
    trips = xml.fromstring(content)
    trip_dict = {'trips' : trips}
    '''
    xml = ET.fromstring(content)
    trips = xml.findall("trips/trip")
    trip_dict = {'trips' : trips}
    '''
    path = os.path.join(os.path.dirname(__file__), 'templates/cleartrip.html')
    self.response.out.write(template.render(path, trip_dict))

class MessageParser(webapp.RequestHandler):

  def get(self):
    messages = twitter.statuses.mentions()
    mentions = {'messages':{}}
    counter = 0
    for message in messages:
      msg = re.search('#ping', str(message))
      if msg is not None:
        msgout = msg.group(0)
        if msgout is not None:
          mentions['messages'][('%s' % counter)] = message
          counter += 1
          
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
          
    
    path = os.path.join(os.path.dirname(__file__), 'templates/messages.html')
    self.response.out.write(template.render(path, mentions))

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([
  ('/', MainHandler),
  ('/kayak', KayakHandler),
  ('/cleartrip', ClearTripHandler),
  ('/cron', CronHandler),
  ('/api/kayak', KayakApi),
  ('/messaging', MessageParser),
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()


