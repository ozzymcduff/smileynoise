import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp

from model import *
from django.utils import simplejson
from smileys import SmileysValidation
from urlhelper import urlencode,urldecode
import urllib

def str_to_long(_id):
	id = int(_id) if _id != '' else None
	return id

class ViewMessage(webapp.RequestHandler):
	def get(self,value):
		ids=None
		try:
			ids=int(value)
		except ValueError:
			pass
		if ids:#support both int id and url encoded smiley
			item = Message.get_by_id(ids=ids,parent=None)
		else:
			item = Message.gql("WHERE value = :value",value=urldecode(value)).get()

		if item:
			self.response.out.write(template.render('views/message/view.html',\
				{ 'data':item,\
				  'url': urllib.quote_plus("http://smileynoise.appspot.com/view/"+str(item.key().id())),\
				  'urlid': urlencode(item.value)\
				}))
		else:
			missing_view = 'views/message/missing_id.html' if ids else 'views/message/missing_smiley.html'

			self.error(404)
			self.response.out.write(template.render(missing_view,\
				{ 'urlid': value,\
				  'id': urldecode(value)\
				}))

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
		item = self.Type.get_by_id(ids=id,parent=None) if id else {'id':"",'value':self.request.get('value')}
		if id: item.assert_access()
		self.response.out.write(template.render('views/message/edit.html',{'data':item,'type':pagetype}))
	def post(self,pagetype,id):
		id = str_to_long( id)
		self.assert_type(id,pagetype)
		errors = []
		value=self.request.get('value')
		if not  SmileysValidation().isValid(value):
			errors.append( "Not a smiley!")
		#else:
		if id :
			item = self.Type.get_by_id(ids=id,parent=None)
			item.assert_access()
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
			self.response.out.write(template.render('views/message/edit.html',{'errors':errors, 'data':item,'type':pagetype}))

class ListForm(webapp.RequestHandler):
	def get(self):
		data = db.GqlQuery("""SELECT * 
							FROM Message WHERE writer=:writer
							ORDER BY updated DESC """, writer=users.get_current_user())
		txt = []
		for item in data:
			txt.append({'id':item.key().id(),'value':item.value,'urlid':urlencode(item.value)})
		self.response.out.write(template.render('views/message/list.html',{'messages':txt}))

class ConfirmDelete(webapp.RequestHandler):
	def get(self,id):
		item = Message.get_by_id(ids=int(id),parent=None) 
		item.assert_access()
		self.response.out.write(template.render('views/message/confirmdelete.html',{ 'data':item}))
	def post(self,id):
		item = Message.get_by_id(ids=int(id),parent=None) 
		item.assert_access()
		item.delete()
		self.redirect("/message/")

application = webapp.WSGIApplication([

('/message/(create|edit)/([^\/]*).*', EditMessageForm),
('/message/confirmdelete/([^\/]*).*', ConfirmDelete),
('/view/([^\/]*).*', ViewMessage),
('/message/view/([^\/]*).*', ViewMessage),
('/message/.*', ListForm),

], debug=False)

def main():
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()