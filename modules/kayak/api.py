
from google.appengine.api import urlfetch

class Api(object):

  headers = {}
  deadline = 10
  method = urlfetch.GET
  follow_redirects = False
  session_id = ''
  search_id = ''

  def __init__(self, api_token, domain):
    self.api_token = api_token,
    self.domain = domain

  def get_session(self):
    url = (self.domain + '/k/ident/apisession?token=%s' % self.api_token)
    result = urlfetch.fetch(url=url, method=urlfetch.GET, deadline=10, follow_redirects=False)
    return result

  def post_search(self,origin,destination,depart_date,return_date):
    basicmode = 'true'
    oneway = 'n'
    origin = origin
    destination = destination
    destcode = ""
    depart_date = depart_date
    depart_time = "a"
    return_date = return_date
    return_time = "a"
    travelers = "1"
    cabin = "b"
    action = "doFlights"
    apimode = "1"
    version = "1"
    sid = self.session_id
    url = (self.domain + '/s/apisearch?basicmode=%s&oneway=%s&origin=%s&destination=%s&destcode=%s&depart_date=%s&depart_time=%s&return_date=%s&return_time=%s&travelers=%s&cabin=%s&action=%s&apimode=%s&_sid_=%s&version=%s' % (
      basicmode, oneway, origin, destination, destcode, depart_date, depart_time, return_date, return_time, travelers, cabin, action, apimode, sid, version ))
    
    result = urlfetch.fetch(
      url=url, 
      method=self.method, 
      headers=self.headers, 
      deadline=self.deadline,
      follow_redirects=self.follow_redirects)
    return result
    
  def get_results(self):
    sid = self.session_id
    searchid = self.search_id
    c = "20"
    version = "1"
    apimode  = "1"
    mode = ""
    sort = "price"
    direction = "up"
    url = (self.domain + '/s/apibasic/flight?searchid=%s&c=%s&d=%s&s=%s&apimode=%s&_sid_=%s' % (searchid, c, direction, sort, apimode, sid))
    result = urlfetch.fetch(
      url=url,
      method=self.method, 
      headers=self.headers, 
      deadline=self.deadline,
      follow_redirects=self.follow_redirects)
    return result

class KayakError:
  pass
    
class Kayak(Api):
  def __init__(self, api_token, domain):
    Api.__init__(self, api_token, domain)

__all__ = ["Kayak", "KayakError"]
