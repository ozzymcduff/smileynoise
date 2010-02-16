#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



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
		txt.append({'id':item.key().id(),'value':item.value,'writer':item.writer.nickname()})
	self.response.out.write(template.render('views/main/index.html',{'messages':txt}))


def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
