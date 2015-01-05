from google.appengine.ext import db
from google.appengine.api import users
from model import *
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        data = db.GqlQuery("""SELECT * 
            FROM Message
            ORDER BY updated DESC """)
        txt = []
        for item in data:
            txt.append( Message.toDictionary(item) )

        template = JINJA_ENVIRONMENT.get_template('views/main/index.html')
        self.response.write(template.render({'messages':txt}))


application = webapp2.WSGIApplication(
[('/', MainHandler),\
],debug=True)

