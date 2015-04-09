import webapp2
import cgi
from google.appengine.api import users
import Cookie

MAIN_PAGE_HTML = """\
<html>
  <title>Get me WIFI NOW!</title>
  <body>
    <p>Hi there! Welcome to XXXX, pls type the message given to you</p>
    <form action="/login" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign in to get Free WIFI Now"></div>
    </form>
  </body>
</html>
"""

MAIN_PAGE_HTML_BACK = """\
<html>
  <title>Get me WIFI NOW!</title>
  <body>
    <p>Hi there! Welcome back to XXXX, Pls type in the message given to you</p>
    <form action="/login" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Get me Free WIFI Now"></div>
    </form>
  </body>
</html>
"""

TIME_OUT_FUNCTION = """\
<script type="text/javascript">
       
    function launchiOSApp()  {
        console.log("*********** here **************");
        window.location = "wifi://com.knuggetlabs.patient";
        window.setTimeout(function (){ window.location.replace('itms://phobos.apple.com'); }, 1);
    }
    
    function launchAndroidApp()  {
        console.log("*********** here **************");
        window.location = "wifi://com.knuggetlabs.patient";
        window.setTimeout(function (){ window.location.replace('http://play.google.com'); }, 1);
    }
</script>
"""

class DetectPhone(object):
    def detect(self, request):
        headers = request.headers;
        # print ('Headers: ' + str(headers))
        user_agent = headers.get("User-Agent")
        
        print 'User agent: ' + str(user_agent)
        
        if 'iPhone' in user_agent :
            return "iPhone"
        
        elif 'Android' in user_agent :
            return "android"

        return "Unknown"
        
class MainPage(webapp2.RequestHandler):
    
    def get(self):
        cookie = self.request.cookies.get('getmewifinow')
        print 'Cookie: ' + str(cookie)
        if (cookie is None) :
            self.response.write(MAIN_PAGE_HTML)
            self.response.set_cookie('getmewifinow', 'some_value')
        else :
            self.response.write(MAIN_PAGE_HTML_BACK)
    
class WiFiSigner(webapp2.RequestHandler):
    
    def post(self):
        phoneType = DetectPhone().detect(self.request)
        
        self.message = "worldbest"
        if (self.message == self.request.get('content')) :
            self.response.write('<html><title>Welcome to XXXX, Enjoy your Free WIFI NOW!</title>\n<body>\n')
            self.response.write(TIME_OUT_FUNCTION)
            self.response.write('<p>Detecting phone: ' + phoneType + '</p>')
            self.response.write('\n<p>Detecting if app is installed - next</p>')
            
            if (phoneType == 'android') :
                self.response.write('\n<p>Detecting if app is installed in android - next</p>')
                self.response.write('<p>\nLaunching wifi://knuggetlabs</p>')
                #self.response.write('<meta http-equiv="refresh" content="2; url=wifi://" />')
                self.response.write('<script type="text/javascript">setTimeout(launchAndroidApp, 2000);</script>')
                
            elif (phoneType == 'iPhone') :
                self.response.write('<p>\nDetecting if app is installed in iPhone - next</p>')
                self.response.write('<p>\nLaunching wifi://knuggetlabs</p>')
                #self.response.write('<meta http-equiv="refresh" content="2; url=wifi://" />')
                self.response.write('<script type="text/javascript">setTimeout(launchiOSApp, 2000);</script>')
                
            elif (phoneType == 'iPad') :
                self.response.write('\n<p>Detecting if app is installed in iPad - next</p>')

            else :
                self.response.write('\n<p>Need to handle</p>')
                self.response.write('<script type="text/javascript">setTimeout(launchAndroidApp, 2000);</script>')
            
            self.response.write('</body></html>')

        else:
            self.response.write('<html><body>You wrote:<pre>')
            self.response.write(cgi.escape(self.request.get('content')))
            self.response.write('</pre> which does not match the message of the day, pls check again</body></html>')
        
    
app = webapp2.WSGIApplication([
            ('/', MainPage),
            ('/login', WiFiSigner)], debug=True)