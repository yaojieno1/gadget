from bottle import Bottle, run, request

import sae

app = Bottle()

@app.get("/:url#.+#")
def hello(url):
    print "GET url:  /" + url + " from remote ip [" + request['REMOTE_ADDR'] + "] by User-Agent [" + request.environ.get('HTTP_USER_AGENT','no agent') +"]"
    return "Hello, world! - GET"

@app.post("/:url#.+#")
def posthello(url):
    print "POST url: /" + url + " from remote ip [" + request['REMOTE_ADDR'] + "] by User-Agent [" + request.environ.get('HTTP_USER_AGENT','no agent') +"]"
    postValue =  request.body.read()
    print "POST body: " + postValue
    return "Hello, World - POST"


application = sae.create_wsgi_app(app)
