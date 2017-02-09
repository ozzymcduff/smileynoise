#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp

class NotFoundHandler(webapp.RequestHandler):

  def get(self):
    self.response.write('Not found!')


def main():
  application = webapp.WSGIApplication([('/.*', NotFoundHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()

