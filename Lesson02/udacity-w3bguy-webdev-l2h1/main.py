#!/usr/bin/env python
import webapp2
import cgi

basicPage="""
  <form method="post">
    <h2>Enter Some Text To ROT13</h2>
    <textarea name="text" id="text">%(enteredText)s</textarea>
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

# END UTILITY FUNCTIONS
###########################################################################################################

class MainHandler(webapp2.RequestHandler):
  def writeForm(self,error="",enteredText=""):
    self.response.out.write(basicPage % {"error":error,
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
  
app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
