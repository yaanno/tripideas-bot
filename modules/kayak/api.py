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
  
  def post_search(self,sid):
    oneway = "n"
    origin = "LON"
    destination = "MAD"
    destcode = ""
    depart_date = "06/20/2009"
    depart_time = "a"
    return_date = "06/26/2009"
    return_time = "a"
    travelers = "1"
    cabin = "b"
    action = "doflights"
    apimode = "1"
    version = "1"
    url = (self.domain + '/s/apisearch?basicmode=true&oneway=%s&origin=%s&destination=%s&destcode=%s&depart_date=%s&depart_time=%s&return_date=%s&return_time=%s&travelers=%s&cabin=%s&action=%s&apimode=%s&_sid_=%s&version=%s' % (
      oneway, 
      origin, 
      destination, 
      destcode, 
      depart_date, 
      depart_time, 
      return_date, 
      return_time, 
      travelers, 
      cabin, 
      action, 
      apimode,
      sid,
      version
    ))
    return url
    #result = urlfetch.fetch(url)
    #return result.content
  '''
  /s/apisearch?
    basicmode=true&
    oneway=n&
    origin=BOS&
    destination=SFO&
    destcode=&
    depart_date=04/09/2006&
    depart_time=a&
    return_date=04/13/2006&
    return_time=a&
    travelers=2&
    cabin=b&
    action=doflights&
    apimode=1&
    _sid_=1-kjdfsh2iu3d888823
  '''
  def get_results(self, sid, searchid):
    searchid = searchid
    sid = sid
    c = "10"
    version = "1"
    apimode  = "1"
    mode = ""
    sort = "price"
    direction = "down"
    url = (self.domain + '/s/apibasic/flight?searchid=%s&c=%s&m=%s&d=%s&s=%s&apimode=%s&_sid_=%s&version=%s' % (searchid, c, mode, direction, sort, apimode, sid, version))
    result = urlfetch.fetch(url)
    return result.content

class KayakError:
  pass
    
class Kayak(Api):
  def __init__(self, api_key, domain):
    Api.__init__(self, api_key, domain)

__all__ = ["Kayak", "KayakError"]