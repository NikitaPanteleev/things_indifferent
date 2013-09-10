#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Things-indifferent is a small web-application for creating courses. It provides such features as:
yes - user registration
no  - simple blog system (with comments)
no  - user profiles (they are made according ot gamifacation theory)
no  - course creator and course catalog
"""
__author__ = 'Nikita Panteleev'
__version__ = '1.05'
__license__ = 'MIT'

import os
#import re
import urllib
import webapp2

#-----------------------------------
from google.appengine.ext import db

#Base handler
import lib.bloghandler as bloghandler
#database
import db.user as db_user
import db.post as db_post
#blog handlers
from lib.blog import BlogFront  #Front page of the blog
from lib.blog import PostPage   #Rendering the particular post page
from lib.blog import NewPost    #Creating new post
#authentication handlers
from lib.auth import Register
from lib.auth import Login
from lib.auth import Logout


class MainPage (bloghandler.BlogHandler):
    def get (self):
        self.render ('base.html',simple_text = "Things indifferent. Use it. Learn it. Love it.",
                                title = "Lluvioso Septiembre"
                                )


class Welcome(bloghandler.BlogHandler):
    def get(self):
        if self.user:
            self.render('base.html', simple_text = "Welcome, %s!"%(self.user.name),
                                     title = "Things indifferrent",)
        else:
            self.redirect('/signup')

class Profile(bloghandler.BlogHandler):
    def get (self,user):
        self.render ("profile.html", user = user,
                                  title = "Things indifferrent",
                        )
application = webapp2.WSGIApplication(
    [('/', MainPage),
    ('/home/?', MainPage),
    ('/community/(\w+)/post/([0-9]+)(?:.json)?/?', PostPage),
    ('/community/(\w+)(?:/blog)?(?:.json)?/?',BlogFront),
    ('/community/(\w+)(?:/profile)/?',Profile),
    ('/community/blog/newpost/?', NewPost),
    ('/signup/?', Register),
    ('/login/?', Login),
    ('/logout/?', Logout),
    ('/welcome/?', Welcome),

    ],
    debug=True)

