#!/usr/bin/env python

from google.appengine.api import urlfetch

class Api(object):
  def __init__(self, api_key, domain):
    self.api_key = api_key,
    self.domain = domain
  
  def get_session(self):
    url = (self.domain + '/k/ident/apisession?token=%s' % self.api_key)
    result = urlfetch.fetch(url)
    return result.content
  
  def post_search():
    url = (self.domain + '/k/ident/apisession?token=%s' % self.api_key)
    result = urlfetch.fetch(url)
    return result.content
  
  def get_results():
    return

class KayakError:
  pass
    
class Kayak(Api):
  def __init__(self, api_key, domain):
    Api.__init__(self, api_key, domain)

__all__ = ["Kayak", "KayakError"]