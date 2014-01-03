import os
import webapp2
import jinja2
import hashlib
import hmac
from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__), 'lib/html')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

#def hash_str(s):
#  return hashlib.md5(s).hexdigest()
SECRET = 'ASDGfw43563426%^$%#@T^@#$gv2%$&#$^GVQEVSERy34567436thweryh34&#$%THW&^#5j3w5ynb356h5b656h#%^U'
def hash_str(s):
    ###Your code here
    return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
  return "%s|%s" % (s,hash_str(s))

def check_secure_val(h):
    hSplit=h.split('|')
    return hSplit[0] if make_secure_val(hSplit[0])==h else None

class Handler(webapp2.RequestHandler):
  def write(self,*a,**kw):
    self.response.out.write(*a,**kw)
  
  def render_str(self,template,**params):
    t=jinja_env.get_template(tempalte)
    return t.render(params)
  
  def render(self,template,**kw):
    self.write(self.render_str(template,**kw))
  
class MainPage(Handler):
  def get(self):
    self.response.headers['content-Type']='text/html'
    visits = 0
    visit_cookie_str=self.request.cookies.get('visits') # cookie dictionary, if there, get value, if not default to 0
    self.write("<br />visit_cookie_str: "+str(visit_cookie_str))
    if visit_cookie_str:
      self.write("<br />visit_cookie_str: "+str(visit_cookie_str))
      cookie_val = check_secure_val(str(visit_cookie_str))
      self.write("<br />cookie_val: "+str(cookie_val))
      if cookie_val:
        self.write("<br />cookie_val: "+cookie_val)
        visits = int(cookie_val)
        
    visits+=1
    
    new_cookie_val = make_secure_val(str(visits))
    self.write("<br />new_cookie_val: "+new_cookie_val)
    self.response.headers.add_header('Set-Cookie','visits=%s' % new_cookie_val)
    
    if visits > 100:
      self.write("<br /><br />You are awesome (%s visits)" % visits)
    else:
      self.write("<br /><br />You've been here %s times!" % visits)

app = webapp2.WSGIApplication([
                               ('/', MainPage)
                              ], debug=True)
