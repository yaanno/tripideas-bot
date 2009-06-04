#!/usr/bin/env python

SETTINGS = {
  'BASE_URL' : 'http://www.kayak.com',
  'API_KEY' : 'J4u2pGhCXG_weKCEzKVdHQ'
}

import os
import re
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from modules import twitter as t
from modules import simplejson as j
from modules import kayak as k

twitter = t.Twitter("tripideas","stledi6v", format="json")
kayak = k.Kayak(SETTINGS['API_KEY'], SETTINGS['BASE_URL'])

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
    kayak_session = kayak.get_session()
    self.response.out.write('<textarea cols="50" rows="10"> %s </textarea>' % kayak_session)
    
    p = re.search("sid>(.*)</sid", kayak_session)
    p = p.group(1)
    self.response.out.write('<textarea cols="50" rows="10"> %s </textarea>' % p)
    
    '''
    kayak_session = xml.etree.ElementTree.XML(kayak_session)
    m = kayak_session.items()
    out = kayak_session
    self.response.out.write('<textarea> %s </textarea>' % m)
    self.response.out.write('<textarea> %s </textarea>' % out)
    '''

def main():
  application = webapp.WSGIApplication([
  ('/', MainHandler),
  ('/api', ApiHandler)
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

import types
import pprint

def getMethods(object):
    methods = []
    names = dir(object.__class__)
    for name in names:
        m = getattr(object.__class__, name)
        if isinstance(m, types.MethodType):
            #print "method:", m
            methods.append(m)
    return methods

if __name__ == '__main__':
  main()
