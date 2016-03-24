from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import common gateway interface
import cgi
import RestaurantManager

# handler -- specify what to do based on type of request
class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>List of All Restaurants</h1>"

                restaurants = RestaurantManager.getRestaurants()

                for restaurant in restaurants:
                    output += "<p>"
                    output += restaurant.name+" (ID "+str(restaurant.id)+")"
                    output += "</p>"
                
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola! <a href = '/hello' "\
                          ">Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' "\
                          "action='/hello'><h2>What would you like me to say?"\
                          "</h2><input name='message' type='text' ><input "\
                          "type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            # parse an html header into a main value and a dictionary of params
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            # check if the data is form data, do the post if so
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' "\
                          "action='/hello'><h2>What would you like me to say?"\
                          "</h2><input name='message' type='text' ><input "\
                          "type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
        except:
            pass

# instantiate server and specify port
def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

# interpreter will run main method
if __name__ == '__main__':
    main()
