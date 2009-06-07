'''
SETTINGS = {
  'Kayak': {
    'BASE_URL' : 'http://api.kayak.com',
    'API_TOKEN' : 'J4u2pGhCXG_weKCEzKVdHQ',
  },
  'Cleartrip' : {
    'BASE_URL' : 'http://api.staging.cleartrip.com/air/1.0/search',
    'API_KEY' : '811e539ed2bb674449d3fc776b7c70ce',
  },
  'Tripideas' : {
    'username' : 'tripideas',
    'password' : 'stledi6v',
    'format' : 'json',
  }
}
'''
import os
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

class ApiHandler(webapp.RequestHandler):
  def get(self):
    pass
    
    
def main():
  application = webapp.WSGIApplication([
  ('/', MainHandler),
  ('/api', ApiHandler)
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()


