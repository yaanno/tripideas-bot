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


