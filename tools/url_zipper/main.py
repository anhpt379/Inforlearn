#!/usr/bin/env python


"""A url-shortener built on Google App Engine."""
__author__ = 'AloneRoad'

""" 
All Urly records in the database have an id and an href. We base62 that
integer id to create a short code that represents that Urly.

Format options are: json, xml, html, and txt

/{code}                     Redirect user to urly with this code
/{code}(.format)            Show user formatted urly with this code
/new(.format)?href={href}   Create a new urly with this href or
                            return existing one if it already exists
                            Note special handling for 'new' code
                            when we have a href GET parameter 'cause
                            'new' by itself looks like a code
"""
import wsgiref.handlers
import re, os, logging
from google.appengine.ext import webapp
from google.appengine.ext import db
from urly import Urly
from view import MainView

class MainHandler(webapp.RequestHandler):
    """All non-static requests go through this handler.
    The code and format parameters are pre-populated by
    our routing regex... see main() below.
    """
    def get(self, code, format):
        try:
            if (code is None):
                MainView.render(self, 200, None, format)
                return
            href = self.request.get('href').strip().encode('utf-8')
            title = self.request.get('title').strip().encode('utf-8')
            if (code == 'new') and (href is not None):
                try:
                    u = Urly.find_or_create_by_href(href)
                    if u is not None:
                        MainView.render(self, 200, u, format, href, title)
                    else:
                        logging.error("Error creating urly by href: %s", str(href))
                        MainView.render(self, 400, None, format, href)
                except db.BadValueError:
                    # href parameter is bad
                    MainView.render(self, 400, None, format, href)
            else:
                u = Urly.find_by_code(str(code))
                if u is not None:
                    MainView.render(self, 200, u, format)
                else:
                    MainView.render(self, 404, None, format)
        except:
            MainView.render(self, 404, None, format)
    
    def head(self, code, format):
        if (code is None):
            self.error(400)
        else:
            u = Urly.find_by_code(str(code))
            if u is not None:
                self.redirect(u.href)
            else:
                self.error(404)

def main():
    application = webapp.WSGIApplication([
        ('/([a-zA-Z0-9]{1,6})?(.xml|.json|.html|.txt)?', MainHandler)
    ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
