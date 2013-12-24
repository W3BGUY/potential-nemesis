import webapp2

form="""
  <form method="post" >
    What is your birthday?
    <br />
    <label> Month
      <input type="text" name="month" value="%(uMonth)s"/>
    </label>
    <label> Day
      <input type="text" name="day" value="%(uDay)s"/>
    </label>
    <label> Year
      <input type="text" name="year" value="%(uYear)s"/>
    </label>
    <br />
    <div style="color:red;">%(error)s</div>
    <br /><br />
    <input type="submit" />
  </form>
"""

###########################################################################################################
# BEGIN UTILITY FUNCTIONS

# MONTH VALIDATION 
fullMonths = ['January','February','March','April','May','June','July','August','September','October','November','December']
monthAbbvs = dict((m[:3].lower(), m) for m in fullMonths)

def validMonth(month):
  if month:
    shortMonth=month[:3].lower()
    return monthAbbvs.get(shortMonth)

# DAY VALIDATION
def validDay(day):
    if day and day.isdigit():
        day=int(day)
        if day>0 and day<32:
            return day

# YEAR VALIDATION
def validYear(year):
    if year and year.isdigit():
        year=int(year)
        if year>=1900 and year<=2020:
            return year

# STRING SUBSTITUTION
givenString1 = "I think %s is a perfectly normal thing to do in public."
def sub1(s):
  return givenString %s

givenString2 = "I think %s and %s are perfectly normal things to do in public."
def sub2(s1,s2):
  return givenString2 %(s1,s2)

given_string3 = "I'm %(nickname)s. My real name is %(name)s, but my friends call me %(nickname)s."
def sub3(name, nickname):
    return given_string3 %{"nickname":nickname,"name":name}

# ESCAPING HTML
import cgi
def escapeHTML(s):
  #for (i,o) in (('&','&amp;'),
  #              ('>','&gt;'),
  #              ('<','&lt;'),
  #              ('"','&quot;')):
  #  s=s.replace(i,o)
  #return s
  return cgi.escape(s, quote=True)

# END UTILITY FUNCTIONS
###########################################################################################################


class MainPage(webapp2.RequestHandler):
  def writeForm(self,error="",uMonth="",uDay="",uYear=""):
    self.response.out.write(form % {"error":error,
                                    "uMonth":escapeHTML(uMonth),
                                    "uDay":escapeHTML(uDay),
                                    "uYear":escapeHTML(uYear)})
  
  def get(self):
    self.writeForm()
  
  def post(self):
    userMonth = self.request.get('month')
    userDay = self.request.get('day')
    userYear = self.request.get('year')
    
    month = validMonth(userMonth)
    day = validDay(userDay)
    year = validYear(userYear)
    
    if not (month and day and year):
      self.writeForm("That does not look valid to me",userMonth,userDay,userYear)
    else:
      self.redirect("/thanks")

class thanksHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/thanks', thanksHandler)],debug=True)


