from google.appengine.ext import db
from google.appengine.api import users
from model import *
import wsgiref.handlers
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from urlhelper import urlencode,urldecode
import urllib


class MainHandler(webapp.RequestHandler):
	def get(self):
		data = db.GqlQuery("""SELECT * 
						FROM Message
						ORDER BY updated DESC """)
		txt = []
		for item in data:
			txt.append({'id':item.key().id(),'value':item.value,\
				'writer':item.writer.nickname(),\
				'urlid': urlencode(item.value) } )#http://localhost:8085/view/%3A%E2%82%AC
		self.response.out.write(template.render('views/main/index.html',{'messages':txt}))

class ViewMessage(webapp.RequestHandler):
	def get(self,id):
		ids=None
		try:
			ids=int(id)
		except ValueError:
			pass
		if ids:
			item = Message.get_by_id(ids=ids,parent=None)
		else:
			ids = urldecode(id)
			item = Message.gql("WHERE value = :value",value=ids).get()
		self.response.out.write(template.render('views/main/view.html',\
			{ 'data':item,\
			  'url': urllib.quote_plus("http://smileynoise.appspot.com/view/"+str(item.key().id())),\
			  'urlid': urlencode(item.value)\
			}))


def main():
  application = webapp.WSGIApplication(
	[('/', MainHandler),\
	('/view/([^\/]*).*', ViewMessage)
	],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
