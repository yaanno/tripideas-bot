import os
import re
from settings import *
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from modules import twitter as tw

'''
from modules import simplejson as j
'''

twitter = tw.Twitter(
  SETTINGS['Tripideas']['username'], 
  SETTINGS['Tripideas']['password'], 
  format=SETTINGS['Tripideas']['format']
)

from modules import kayak

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
    
    session_id = re.search('<sid>(.*?)</sid>', kayak_session.content)
    session_id = session_id.group(1)
    
    kayak.session_id = session_id
    kayak.headers = { 'Cookie' : kayak_session.headers['set-cookie'] }
    
    kayak_search = kayak.post_search()
    
    #self.response.out.write('<div style="float:left"><label>Get search:</label><br><textarea cols="50" rows="10">%s</textarea></div>' % kayak_search.content)
    
    
    search_id = re.search('<searchid>(.*?)</searchid>', kayak_search.content)
    search_id = search_id.group(1)
    
    #self.response.out.write('<div style="float:left"><label>Search ID:</label><br><textarea cols="50" rows="10">%s</textarea></div>' % search_id)
    
    kayak.search_id = search_id
    kayak_results = kayak.get_results()
    
    self.response.out.write('<div style="float:left"><label>Search results:</label><br><textarea cols="50" rows="10">%s</textarea></div>' % kayak_results.content)

    result_set = []
 
    more_pending = re.search('<morepending>true</morepending>',kayak_results.content)
    
    if more_pending.group(0) is not None:
      more_pending = True
    
    if more_pending:
      kayak.cycle_poll(result_set)
      
      kayak_results = kayak.get_results()
      result_set.append(kayak_results.content)
      
    self.response.out.write('<div style="float:left"><label>Search results:</label><br><textarea cols="50" rows="10">%s</textarea></div>' % result_set)


def main():
  application = webapp.WSGIApplication([
  ('/', MainHandler),
  ('/cron', CronHandler),
  ('/api/kayak', KayakApi)
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()


