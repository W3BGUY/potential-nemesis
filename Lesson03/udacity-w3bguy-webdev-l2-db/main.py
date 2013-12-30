#!/usr/bin/env python
import webapp2
import cgi
import os
import jinja2
import re

from google.appengine.ext import db

###########################################################################
## BEGIN BASE TEMPLATING CODE

template_dir = os.path.join(os.path.dirname(__file__),'lib')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

def render_str(template,**params):
  t = jinja_env.get_template(template)
  return t.render(params)

class BaseHandler(webapp2.RequestHandler):
  def render(self,template,**kw):
    self.response.out.write(render_str(template,**kw))
  
  def write(self,*a,**kw):
    self.response.out.write(*a,**kw)

## END BASE TEMPLATEING CODE
###########################################################################

class test(BaseHandler):
  def get(self):
    self.render('html/test.htm',testVariable="data From Main")

###########################################################################
## BEGIN DEFAULT APPLICATION CODE

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/unit3/test', test)
], debug=True)

## END DEFAULT APPLICATION CODE
###########################################################################