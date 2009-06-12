import datetime
from google.appengine.ext import db

class Author(db.Model):
  author_id = db.IntegerProperty()
  protected = db.BooleanProperty()
  name = db.StringProperty()
  screen_name = db.StringProperty()

class Message(db.Model):
  body = db.TextProperty()
  message_id = db.IntegerProperty()
  reply_id = db.IntegerProperty()
  author = db.ReferenceProperty(Author)

class Iata(db.Model):
  iata = db.StringProperty()
  city = db.StringProperty()
  country = db.StringProperty()
  airport = db.StringProperty()

class Search(db.Model):
  user = db.ReferenceProperty(Author)
  message = db.ReferenceProperty(Message)

class Job(db.Model):
  status = db.StringProperty()
  
  