import urllib2
from HTMLParser import HTMLParser
from time import strftime
import requests

def getUrlData(url):
    return urllib2.urlopen(url).read()
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    htmlData = []
    imgList = []
    linkList = []
    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        if(tag=='img' and attrs[0][0] =='src' and '.jpg' in attrs[0][1]):
            #print "Encountered a start tag:", tag
            self.imgList.append('http:'+ attrs[0][1])
            self.linkList.append(attrs[0][1])
        pass
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        pass
    def handle_data(self, data):
        #print "Encountered some data  :", data
        if('www' in data and 'script' not in data):
            self.htmlData.append(data)


html = ''
attempt = 10

while (attempt>0):
 try:
     html = getUrlData("http://www.reddit.com")
     print html
     break
 except urllib2.HTTPError as err:  # Python 2.5 syntax
     print "Oops!  Too Many Requests.  Try again..."
     attempt-=1

# instantiate the parser and fed it some HTML
if (len(html)>0):
    parser = MyHTMLParser()
    parser.feed(html)

print parser.imgList

if(parser):
    s = '<html><body>'
    for (i, item) in enumerate(parser.imgList):
        s += "<a href='" + item +"'><img src='" + item + "' /></a>" + "\n"
    s += '</body></html>'

#logging
logfile = strftime("mylogfile_%H_%M_%m_%d_%Y.log")
out_file = open(logfile,"w")
out_file.write(s)
out_file.close()

RECIPIENT = ""; 
MAILGUN_API_KEY = ""
MAILGUN_CALLBACK = ""
SENDER = ""

#send by email the same content
request=requests.post(
    MAILGUN_CALLBACK,
    auth=("api", MAILGUN_API_KEY),
    data={"from": SENDER,
          "to": RECIPIENT,
          "subject": "Hello, new report!",
          "text": s,
          "html": s})

print "Status: {0}".format(request.status_code)
print "Body:   {0}".format(request.text)