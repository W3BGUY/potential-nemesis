##############################
## Unit 03 Homework
## Build a Blog
## 1. Front page that lists entries
## 2. Form to submit new entries (title and blog body required)
## 3. Permalink page for entries to be displayed.
## /newpost   ->  add post
## /blog      ->  front
## Must be POST
## Form inputs must be named: subject and content
## 
## blogDB       -> Blog database
## blogSubject  -> Blog subject variable
## blogContent  -> Blog content variable
## postCreated  -> Blog post date variable
## blogDBO      -> Blog DB cursor
## 
##############################

import webapp2
import cgi
import os
import jinja2
import re

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'lib/html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class blogHandler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
  
  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

def blog_key(name='default'):
  return db.Key.from_path('blogs',name)

class blogDB(db.Model):
  blogSubject = db.StringProperty(required = True)
  blogContent = db.TextProperty(required = True)
  postCreated = db.DateTimeProperty(auto_now_add = True)
  postLastMidified = db.DateTimeProperty(auto_now = True)
  
  def render(self):
    return render_str("w3bguy_blog_post.htm", p=self)

class blogPost(blogHandler):
  def get(self,post_id):
    key=db.Key.from_path('blogDB',int(post_id))
    postID=db.get(key)
    
    if not postID:
      self.error(404)
      return
    
    self.render("w3bguy_blog_permalink.htm",post=post)

class blogNewPost(blogHandler):
  def render_front(self, blogSubject="",blogContent="",error=""):
    blogDBO = db.GqlQuery("SELECT * FROM blogDB ORDER BY postCreated DESC")
    
    self.render("w3bguy_blog_newPost.htm", blogSubject=blogSubject,blogContent=blogContent,error=error,blogDBO=blogDBO)
  
  def get(self):
    self.render_front();
  
  def post(self):
    blogSubject = self.request.get("subject")
    blogContent = self.request.get("content")
    
    if blogSubject and blogContent:
      b = blogDB(blogSubject=blogSubject,blogContent=blogContent)
      b.put()
      self.redirect("/blog/%s" % str(b.key().id()))
    else:
      error = "We need both a subject and some content!"
      self.render_front(blogSubject,blogContent,error)

class blogFront(blogHandler):
  def get(self):
    blogDBO = db.GqlQuery("SELECT * FROM blogDB ORDER BY postCreated DESC")
    #blogDBO = blogDB.all().order('-created')   #different way of writing the above statement.
    self.render("w3bguy_blog.htm",blogDBO=blogDBO)

app = webapp2.WSGIApplication([('/blog', blogFront),
                               ('/blog/?',blogFront),
                               ('/blog/([0-9]+)',blogPost), #any integers 0-9
                               ('/blog/newpost',blogNewPost)
                               ], debug=True)
