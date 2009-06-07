from google.appengine.api import urlfetch

class Api(object):

  def __init__(self, api_token, domain):
    self.api_token = api_token,
    self.domain = domain
  
  def do_search(self):
    from_city = 'BUD'
    to = 'LON'
    depart_date = '2009-07-10'
    return_date = '2009-08-10'
    
    url = (self.domain + '?from=%s&to=%s&depart-date=%s&return-date=%s' % (from_city, to, depart_date, return_date))
    headers = {'X-CT-API-KEY': self.api_token}
    
    result = urlfetch.fetch(url=url, method=urlfetch.GET, headers = {'X-CT-API-KEY': '811e539ed2bb674449d3fc776b7c70ce'}, deadline=10)
    
    return result.content

class ClearTripError:
  pass
    
class ClearTrip(Api):
  def __init__(self, api_token, domain):
    Api.__init__(self, api_token, domain)

__all__ = ["ClearTrip", "ClearTripError"]
