from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from read_database import get_restaurants
from new_restaurant import create_restaurant, reset_name, delete_restaurant


#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Restaurant


#engine = create_engine('sqlite:///restaurantmenu.db')
#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith('/restaurants/new'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = '''<html><body>
                <h1>Make a New Restaurant</h1>
                <form method="POST" enctype="multipart/form-data"
                action="/restaurants/new">
                <input name="newRestaurantName" type="text"
                placeholder="New Restaurant Name">
                <input type="submit" value="Create">
                </body></html>'''
            self.wfile.write(output)
            return

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += '''<html><body><h1><a href="/restaurants/new">
                    Make a new Restaurant</a></h1>'''
            output += "<ul>"
            restaurants = get_restaurants()

            for restaurant in restaurants.keys():
                output += "<li>{}".format(restaurants[restaurant])
                output += '''<br><a href="/restaurants/{}/edit">Edit</a>
                    <br><a href="/restaurants/{}/delete">Delete</a></li><br>
                    </ul>
                    </html></body>'''.format(restaurant, restaurant)
            self.wfile.write(output.encode())
            print(output)
            return

        if self.path.endswith('/edit'):
            restaurant_id = int(self.path.split('/')[2])
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            restaurants = get_restaurants()
            if restaurant_id in restaurants:
                output = '''<html><body>
                    <h1>{}</h1>
                    <form method="POST" enctype="multipart/form-data"
                    action="/resturants/{}/edit">
                    <input name="newRestaurantName" type="text"
                    placeholder="{}">
                    <input type="submit" value="Rename"></form>
                    '''.format(
                            restaurants[restaurant_id],
                            restaurant_id,
                            restaurants[restaurant_id]
                        )
                self.wfile.write(output)

        if self.path.endswith('/delete'):
            restaurant_id = int(self.path.split('/')[2])
            restaurants = get_restaurants()
            if restaurant_id in restaurants:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '''<html><body>
                    <h1>Are you sure you want to delete {}?</h1>
                    <form method="POST" enctype="multipart/form-data"
                    action="/restaurants/{}/delete">
                    <input type="submit" value="Delete"></form></body></html>
                    '''.format(restaurants[restaurant_id], restaurant_id)
                self.wfile.write(output)

    def do_POST(self):
        if self.path.endswith('/edit'):
            ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type')
                    )
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurant_id = self.path.split('/')[2]
                reset_name(restaurant_id, messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        if self.path.endswith("/restaurants/new"):
            ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type')
                    )
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                #newRestaurant = Restaurant(name=messagecontent[0])
                #session.add(newRestaurant)
                #session.commit()
                create_restaurant(messagecontent[0])

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

        if self.path.endswith('/delete'):
            ctype, pdict = cgi.parse_header(
                    self.headers.getheader('Content-type')
                )
            restaurant_id = str(self.path.split('/')[2])
            delete_restaurant(restaurant_id)
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

            #self.send_response(301)
            #self.end_headers()

            #ctype, pdict = cgi.parse_header(self.headers.getheader(
            #    'content-type'
            #    )
            #)
            #if ctype == 'multipart/form-data':
            #    fields = cgi.parse_multipart(self.rfile, pdict)
            #    messagecontent = fields.get('output')

            #output = ""
            #output += "<html><body>"
            #output += " <h2> okey, how about this: </h2>"
            #output += "<h1> %s </h1>" % messagecontent[0]
            #output += '''<form method="POST" enctype="multipart/form-data"
            #            action="/hello"><h2>What would you like me to say?</h2>
            #            <input name="output" type="text" >
            #            <input type="submit" value="Submit"></form>'''
            #output += "</html></body>"
            #self.wfile.write(output.encode())
            #print(output)


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
