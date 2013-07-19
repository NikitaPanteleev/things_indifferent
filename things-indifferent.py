# This Python file uses the following encoding: utf-8
import re
import os

import jinja2
import webapp2
import urllib

from google.appengine.ext import db
from data.navigation import navigation
from urlparse import urlparse
from posixpath import basename, dirname



template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#-------------------------------------------------------
#basic display of content, the original class is defined
#-------------------------------------------------------
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
"""
#This part must override error_handler but it doesn't work. Well, the problem isn't in this part of code but in the settings.    
    @classmethod
    def handle_exception(cls,exception, debug_mode):
        _template_parameters = navigation.HeaderParameters
        _template_parameters ['message'] = exception
        super(BaseHandler,cls).render('plain.html',**self._template_parameters)
"""





#-------------------------------------------------------
#initial page handler
#-------------------------------------------------------


class MainPage(BaseHandler):
    _template_parameters = dict(navigation.HeaderParameters) 
    _template_parameters ['SidebarName'] = 'Concepts'
    _template_parameters ['Sidebar'] = navigation.Concepts
    _template_parameters ['username'] = 'Anonymous'
    def get(self):
        url = urlparse(self.request.url).path
        file_name = basename(url)
        if url == '' or url=='/':
            self._template_parameters ["text"] = '<b>Welcome</b>'
            self.render('content.html',**self._template_parameters)
        elif os.path.exists('data/content'+url):
            page = urllib.urlopen('data/content'+url).read()
            self._template_parameters ["text"] = page 
            self.render('content.html',**self._template_parameters)
        else:
            self._template_parameters ["text"] = "Nothing here" 
            self.render('content.html',**self._template_parameters)
            
        

#-------------------------------------------------------
#All Handlers must store here
#-------------------------------------------------------
application = webapp2.WSGIApplication(
    [('/.*', MainPage),
    ],
    debug=True)