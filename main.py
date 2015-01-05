from google.appengine.ext import db
from google.appengine.api import users
from model import *
import wsgiref.handlers
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp


class MainHandler(webapp.RequestHandler):
	def get(self):
		data = db.GqlQuery("""SELECT * 
						FROM Message
						ORDER BY updated DESC """)
		txt = []
		for item in data:
			txt.append( Message.toDictionary(item) )
		self.response.out.write(template.render('views/main/index.html',{'messages':txt}))
			


def main():
	application = webapp.WSGIApplication(
		[('/', MainHandler),\
		],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
