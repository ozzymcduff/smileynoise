from google.appengine.ext import db
from google.appengine.api import users
from model import *
import wsgiref.handlers
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp

import urllib

class MainHandler(webapp.RequestHandler):
	def get(self):
		data = db.GqlQuery("""SELECT * 
						FROM Message
						ORDER BY updated DESC """)
		txt = []
		for item in data:
			txt.append({'id':item.key().id(),'value':item.value,\
				'writer':item.writer.nickname() } )
		self.response.out.write(template.render('views/main/index.html',{'messages':txt}))

class ViewMessage(webapp.RequestHandler):
	def get(self,id):
		item = Message.get_by_id(ids=int(id),parent=None)
		self.response.out.write(template.render('views/main/view.html',{ 'data':item, 'url': urllib.quote_plus("http://smileynoise.appspot.com/view/"+str(item.key().id()))}))


def main():
  application = webapp.WSGIApplication(
	[('/', MainHandler),\
	('/view/([^\/]*).*', ViewMessage)
	],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
