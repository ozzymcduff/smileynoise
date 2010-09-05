import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms
from urlhelper import urlencode,urldecode

class Message(db.Model):
	value = db.StringProperty(multiline=False,required=True)
	writer = db.UserProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	updated = db.DateTimeProperty(auto_now=True)
	def __str__(self):
		return self.value
	def assert_access(self):
		if self.writer != users.get_current_user():
			raise 'no access'
	def toDictionary(item):
		return {'id':item.key().id(),'value':item.value,\
			'writer':item.writer.nickname(),\
			'urlid': urlencode(item.value) }