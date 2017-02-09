import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
import os
import jinja2

from model import *
from smileys import SmileysValidation
from urlhelper import urlencode,urldecode
import urllib
JENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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
			item = None
			for data in db.GqlQuery("""SELECT * 
								FROM Message WHERE value = :value
								ORDER BY updated DESC """,value=urldecode(value)):
				if not item : 
					item = data 
					item.writers =[]
				item.writers.append("%s at %s" % (item.writer,item.updated.date()))

		if item:
			template = JENV.get_template('views/message/view.html')

			self.response.write(template.render(\
				{ 'data':item,\
				  'url': urllib.quote_plus("http://smileynoise.appspot.com/view/"+str(item.key().id())),\
				  'urlid': urlencode(item.value)\
				}))
		else:
			missing_view = 'views/message/missing_id.html' if ids else 'views/message/missing_smiley.html'
			template = JENV.get_template(missing_view)
			self.error(404)
			self.response.write(template.render(\
				{ 'urlid': value,\
				  'id': urldecode(value)\
				}))

class EditMessageForm(webapp.RequestHandler):
	Type = Message
	Home = '/message/'
	def assert_type(self,id,tp):
		if tp== 'create' and id != None :
			raise Exception('New messages should not have an id')
		if tp== 'edit' and id == None :
			raise Exception('When editing messages you must have an id')

	def get(self,pagetype,id):
		id = str_to_long( id)
		self.assert_type(id,pagetype)
		item = self.Type.get_by_id(ids=id,parent=None) if id else {'id':"",'value':self.request.get('value')}
		if id: item.assert_access()
		template = JENV.get_template('views/message/edit.html')
		self.response.write(template.render({'data':item,'type':pagetype}))
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
			template = JENV.get_template('views/message/edit.html')
			self.response.write(template.render({'errors':errors, 'data':item,'type':pagetype}))

class ListForm(webapp.RequestHandler):
	def get(self):
		data = db.GqlQuery("""SELECT * 
							FROM Message WHERE writer=:writer
							ORDER BY updated DESC """, writer=users.get_current_user())
		txt = []
		for item in data:
			txt.append(Message.toDictionary(item))
		template = JENV.get_template('views/message/list.html')
		self.response.write(template.render({'messages':txt}))

class ConfirmDelete(webapp.RequestHandler):
	def get(self,id):
		item = Message.get_by_id(ids=int(id),parent=None) 
		item.assert_access()
		template = JENV.get_template('views/message/confirmdelete.html')
		self.response.write(template.render({ 'data':item}))
	def post(self,id):
		item = Message.get_by_id(ids=int(id),parent=None) 
		item.assert_access()
		item.delete()
		self.redirect("/message/")

application = webapp.WSGIApplication([

('/message/(create|edit)/(.*)', EditMessageForm),
('/message/confirmdelete/(.*)', ConfirmDelete),
('/view/(.*)', ViewMessage),
('/message/view/(.*)', ViewMessage),
('/message/.*', ListForm),

], debug=True)

def main():
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
