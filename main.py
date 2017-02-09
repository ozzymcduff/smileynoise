from google.appengine.ext import db
from google.appengine.api import users
from model import *
import wsgiref.handlers
import os
import jinja2
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
JENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp.RequestHandler):
	def get(self):
		data = db.GqlQuery("""SELECT * 
						FROM Message
						ORDER BY updated DESC """)
		txt = []
		for item in data:
			txt.append( Message.toDictionary(item) )
		template = JENV.get_template('views/main/index.html')
		self.response.write(template.render({'messages':txt}))


def main():
	application = webapp.WSGIApplication(
		[('/', MainHandler),\
		],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
