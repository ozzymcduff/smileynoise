import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp

import re
from model import *
from django.utils import simplejson
from smileys import SmileysValidation

def str_to_long(_id):
	id = int(_id) if _id != '' else None
	return id

class EditMessageForm(webapp.RequestHandler):
	Type = Message
	Home = '/message/'
	def assert_type(self,id,tp):
		if ( not 
			{'create': lambda x: x == None,
			'edit': lambda x: x != None}[tp](id)):
			raise 'fail'

	def get(self,pagetype,id):
		id = str_to_long( id)
		self.assert_type(id,pagetype)
		item = self.Type.get_by_id(ids=id,parent=None) if id else {'id':"",'value':""}
		if id and item.writer != users.get_current_user():
			raise 'no access'
		self.response.out.write(template.render('views/message/edit.html',{'data':item}))
	def post(self,pagetype,id):
		id = str_to_long( id)
		self.assert_type(id,pagetype);
		errors = []
		#item = []
		value=self.request.get('value')
		if not  SmileysValidation().isValid(value):
			errors.append( "Not a smiley!")
		#else:
		if id :
			item = self.Type.get_by_id(ids=id,parent=None)
			if item.writer != users.get_current_user():
				raise 'no access'
			item.value = value
		else:
			item = Message(value=value,writer=users.get_current_user())
			item.writer = users.get_current_user()
		
		if len(errors) == 0:
			# Save the data, and redirect to the view page
			item.put();
			self.redirect(self.Home)
		else:
			# Reprint the form
			self.response.out.write(template.render('views/message/edit.html',{'errors':errors, 'data':item}))


class ListForm(webapp.RequestHandler):
	def get(self):
		data = db.GqlQuery("""SELECT * 
							FROM Message WHERE writer=:writer
							ORDER BY updated DESC """, writer=users.get_current_user())
		txt = []
		for item in data:
			txt.append({'id':item.key().id(),'value':item.value})
		self.response.out.write(template.render('views/message/list.html',{'messages':txt}))

application = webapp.WSGIApplication([

('/message/(create|edit)/([^\/]*).*', EditMessageForm),

('/message/.*', ListForm),

], debug=True)

def main():
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()