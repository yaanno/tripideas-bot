
from google.appengine.api import urlfetch

class Api(object):
  def __init__(self, api_token, domain):
    self.api_token = api_token,
    self.domain = domain
  
  def get_session(self):
    url = (self.domain + '/k/ident/apisession?token=%s' % self.api_token)
    result = urlfetch.fetch(url=url, method=urlfetch.GET, deadline=10, follow_redirects=False)
    return result
  
  def post_search(self,sid,headers):
    basicmode = 'true'
    oneway = 'n'
    origin = "MAD"
    destination = "PAR"
    destcode = ""
    depart_date = "06/19/2009"
    depart_time = "a"
    return_date = "06/26/2009"
    return_time = "a"
    travelers = "1"
    cabin = "b"
    action = "doFlights"
    apimode = "1"
    version = "1"
    url = (self.domain + '/s/apisearch?basicmode=%s&oneway=%s&origin=%s&destination=%s&destcode=%s&depart_date=%s&depart_time=%s&return_date=%s&return_time=%s&travelers=%s&cabin=%s&action=%s&apimode=%s&_sid_=%s&version=%s' % (
      basicmode, oneway, origin, destination, destcode, depart_date, depart_time, return_date, return_time, travelers, cabin, action, apimode, sid, version ))
    
    result = urlfetch.fetch(url=url, method=urlfetch.GET, headers=headers, deadline=10,follow_redirects=False)
    return result
    
    
  def get_results(self, sid, searchid, headers):
    searchid = searchid
    sid = sid
    c = "10"
    version = "1"
    apimode  = "1"
    mode = ""
    sort = "price"
    direction = "down"
    url = (self.domain + '/s/apibasic/flight?searchid=%s&apimode=%s&_sid_=%s' % (searchid, apimode, sid))
    result = urlfetch.fetch(url=url, method=urlfetch.GET, headers=headers, deadline=10,follow_redirects=False)
    return result

class KayakError:
  pass
    
class Kayak(Api):
  def __init__(self, api_token, domain):
    Api.__init__(self, api_token, domain)

__all__ = ["Kayak", "KayakError"]
