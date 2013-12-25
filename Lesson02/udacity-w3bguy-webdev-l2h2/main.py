#!/usr/bin/env python
import webapp2
import cgi
import os
import jinja2
import re

from google.appengine.ext import db

rot13Form="""
  <form method="post">
    <h2>Enter Some Text To ROT13</h2>
    <textarea name="text">%(enteredText)s</textarea>
    <br />
    <input type="submit"/>
  </form>
"""

signupForm="""
  <style>
    .col1{
      width:120px;
      display:block;
      float:left;
      font-weight:bold;
    }
    .col2{
      display:inline;
    }
    .col2 input{
      width:170px;
      background-color:#ccc;
    }
    .col2 input:hover{
      width:170px;
      background-color:#eee;
    }
    .col2 input:focus{
      width:170px;
      background-color:#eee;
    }
    .col3{
      display:inline;
      font-weight:bold;
      color:#f00;
    }
  </style>
  <h2>Signup</h2>
  <form method="post">
    <span class="col1">
      <span>Username</span>
    </span>
    <span class="col2">
      <input type="text" name="username" id="username" value="%(username)s"/>
    </span>
    <span class="col3">
      %(usernameError)s
    </span>
    <br />
    <span class="col1">
      <span>Password</span>
    </span>
    <span class="col2">
      <input type="password" name="password" id="password"/>
    </span>
    <span class="col3">
      %(passwordError)s
    </span>
    <br />
    <span class="col1">
      <span>Verify Password</span>
    </span>
    <span class="col2">
      <input type="password" name="verify" id="verify"/>
    </span>
    <span class="col3">
      %(verifyError)s
    </span>
    <br />
    <span class="col1">
      <span>Email (optional)</span>
    </span>
    <span class="col2">
      <input type="text" name="email" id="email" value="%(email)s"/>
    </span>
    <span class="col3">
      %(emailError)s
    </span>
    <br />
    <input type="submit"/>
  </form>
"""

###########################################################################################################
# BEGIN UTILITY FUNCTIONS

# VALIDATE TEXT
def validText(uText):
  if uText:
    return uText

# ESCAPING HTML
def escapeHTML(s):
  #for (i,o) in (('&','&amp;'),
  #              ('>','&gt;'),
  #              ('<','&lt;'),
  #              ('"','&quot;')):
  #  s=s.replace(i,o)
  #return s
  return cgi.escape(s, quote=True)

# ROT13 THE TEXT
def rotIt(s):
  return s.encode('rot13')

USER_RE=re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validUsername(username):
  return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def validPassword(password):
  return password and PASS_RE.match(password)

#EMAIL_RE=re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]{2,3}$")
EMAIL_RE=re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def validEmail(email):
  return not email or EMAIL_RE.match(email)

# END UTILITY FUNCTIONS
###########################################################################################################

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('Hello world!')

class rot13Handler(MainHandler):
  def writeForm(self,error="",enteredText=""):
    self.response.out.write(rot13Form % {"error":error,
                                    "enteredText":escapeHTML(enteredText)})
  
  def get(self):
    self.writeForm()
  
  def post(self):
    userText = self.request.get('text')
    
    goodText = validText(userText)
    
    if not (goodText):
      self.writeForm("",userText)
    else:
      newText=rotIt(userText)
      self.writeForm("",newText)

class signupHandler(MainHandler):
  def writeForm(self,username="",email="",usernameError="",passwordError="",verifyError="",emailError=""):
    self.response.out.write(signupForm % {"username":escapeHTML(username),
                                          "email":escapeHTML(email),
                                          "usernameError":escapeHTML(usernameError),
                                          "passwordError":escapeHTML(passwordError),
                                          "verifyError":escapeHTML(verifyError),
                                          "emailError":escapeHTML(emailError),
                                         })
  def get(self):
    self.writeForm()
  
  def post(self):
    have_error = False
    username=self.request.get('username')
    password=self.request.get('password')
    verify=self.request.get('verify')
    email=self.request.get('email')
    usernameError=''
    passwordError=''
    verifyError=''
    emailError=''
    
    if not validUsername(username):
      usernameError="That's not a valid username."
      have_error=True
      
    if not validPassword(password):
      passwordError="That wasn't a valid password."
      have_error=True
    elif password!=verify:
      verifyError="Your passwords didn't match."
      have_error=True
    
    if not validEmail(email):
      emailError="That's not a valid email."
      have_error=True
    
    if have_error:
      self.writeForm(username,email,usernameError,passwordError,verifyError,emailError)
    else:
      self.redirect('/unit2/welcome?username='+username)

class welcomeHandler(MainHandler):
  def get(self):
    username=self.request.get('username')
    self.response.write('<h2>Welcome, '+username+'!</h2>')

app = webapp2.WSGIApplication([
                                ('/', MainHandler),
                                ('/unit2/rot13',rot13Handler),
                                ('/unit2/signup',signupHandler),
                                ('/unit2/welcome',welcomeHandler)
                              ],debug=True)