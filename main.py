import os
import re
import logging
import time
from string import replace
from settings import *
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from modules.xml2dict import *
from modules import kayak

from modules.messaging import *


kayak = kayak.Kayak(
  SETTINGS['Kayak']['API_TOKEN'],
  SETTINGS['Kayak']['BASE_URL'],
)

class MainHandler(webapp.RequestHandler):
  def get(self):
    pass
    '''
    messages = twitter.statuses.mentions()
    mydict = {'messages':{}}
    counter = 0
    for message in messages:
      mydict['messages'][('%s' % counter)] = message
      counter += 1
      
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, mydict))
    '''

class CronHandler(webapp.RequestHandler):
  def get(self):
    pass
    

class KayakApi(webapp.RequestHandler):

  def get(self):
    
    messaging = Messaging()
    messaging.collect_messages()
    messaging.process_messages()
    
    kayak_session = kayak.get_session()
    logging.debug(kayak_session.content)
    
    session_id = re.search('<sid>(.*?)</sid>', kayak_session.content)
    session_id = session_id.group(1)
    
    kayak.session_id = session_id
    kayak.headers = { 'Cookie' : kayak_session.headers['set-cookie'] }
    
    kayak_search = kayak.post_search(
      messaging.mentions['from'],
      messaging.mentions['to'],
      messaging.mentions['departure']['day'] + '/' + messaging.mentions['departure']['month'] + '/' + messaging.mentions['departure']['year'],
      messaging.mentions['retour']['day'] + '/' + messaging.mentions['retour']['month'] + '/' + messaging.mentions['retour']['year']
    )
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
    
    messaging = Messaging()
    messaging.collect_messages()
    messaging.process_messages()
    
    self.response.out.write(messaging.mentions)
    
    

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


