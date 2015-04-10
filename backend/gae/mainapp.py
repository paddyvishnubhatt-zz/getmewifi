import webapp2
import cgi
from google.appengine.api import users
import Cookie

TIME_OUT_FUNCTION = """\
<script type="text/javascript">
       
    function launchiOSApp()  {
        console.log("*********** here **************");
        window.location = "wifi://com.vishnubhatt.getmewifi";
        window.setTimeout(function (){ window.location.replace('itms://phobos.apple.com'); }, 10);
    }
    
    function launchAndroidApp()  {
        console.log("*********** here **************");
        window.location = "wifi://com.vishnubhatt.getmewifi";
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

    def run(self):
        cookie = self.request.cookies.get('getmewifinow')
        phoneType = DetectPhone().detect(self.request)
        print 'Cookie: ' + str(cookie)
        if (cookie is None) :
            #self.response.write(MAIN_PAGE_HTML)
            print("First time")
            self.response.set_cookie('getmewifinow', 'some_value')
        else :
            #self.response.write(MAIN_PAGE_HTML_BACK)
            print ("Returning again")
            
        self.runApp(phoneType)     
        
    def get(self):
        self.run()
    
    def post(self):
        self.run()
            
    def lookup(self, ssid):
        retVal = True
        if (ssid == "vishnubhatt") :
            retVal = False
        return retVal
    
    def okayToGo(self, ssid, phoneType):
        self.response.write('<html><title>Welcome to XXXX, Enjoy your Free WIFI NOW! from ' + ssid + '</title>\n<body>\n')
        self.response.write(TIME_OUT_FUNCTION)
        self.response.write('<p>Detecting phone: ' + phoneType + '</p>')
        self.response.write('\n<p>Detecting if app is installed - next</p>')
        if (phoneType == 'android') :
            self.response.write('\n<p>Detecting if app is installed in android - next: ' + ssid + '</p>')
            self.response.write('<p>\nLaunching wifi://getmewifi</p>')
            #self.response.write('<meta http-equiv="refresh" content="2; url=wifi://" />')
            self.response.write('<script type="text/javascript">setTimeout(launchAndroidApp, 2000);</script>')
            
        elif (phoneType == 'iPhone') :
            self.response.write('<p>\nDetecting if app is installed in iPhone - next: ' + ssid + '</p>')
            self.response.write('<p>\nLaunching wifi://getmewifi</p>')
            #self.response.write('<meta http-equiv="refresh" content="2; url=wifi://" />')
            self.response.write('<script type="text/javascript">setTimeout(launchiOSApp, 2000);</script>')
            
        elif (phoneType == 'iPad') :
            self.response.write('\n<p>Detecting if app is installed in iPad - next</p>')
    
        else :
            self.response.write('\n<p>Need to handle</p>')
            self.response.write('<script type="text/javascript">setTimeout(launchAndroidApp, 2000);</script>')
        
        self.response.write('</body></html>')
    
    def denyToGo(self):
        self.abort(401)
        
    def runApp(self, phoneType):
        wifiSSId = self.request.get('content')
        print("wifiSSId: " + wifiSSId)
        if (self.lookup(wifiSSId)) :
            self.okayToGo(wifiSSId, phoneType)
        else :
            self.denyToGo()
   
app = webapp2.WSGIApplication([
    ('/', MainPage)], debug=True)
        