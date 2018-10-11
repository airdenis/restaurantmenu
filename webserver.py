from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from read_database import get_restaurants


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>Hello!</body></html>"
            output += '''<form method="POST" enctype="multipart/form-data"
                        action="/hello"><h2>What would you like me to say?</h2>
                        <input name="output" type="text" >
                        <input type="submit" value="Submit"></form>'''
            output += "</html></body>"
            self.wfile.write(output.encode())
            print(output)
            return

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += '''<html><body>&#161Hello! <a href = '/hello' >
                        Back to Hello</a>'''
            output += '''<form method="POST" enctype="multipart/form-data"
                        action="/hello"><h2>What would you like me to say?</h2>
                        <input name="output" type="text" >
                        <input type="submit" value="Submit"></form>'''
            output += "</html></body>"
            self.wfile.write(output.encode())
            print(output)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader(
                'content-type'
                )
            )
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('output')

            output = ""
            output += "<html><body>"
            output += " <h2> okey, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method="POST" enctype="multipart/form-data"
                        action="/hello"><h2>What would you like me to say?</h2>
                        <input name="output" type="text" >
                        <input type="submit" value="Submit"></form>'''
            output += "</html></body>"
            self.wfile.write(output.encode())
            print(output)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
