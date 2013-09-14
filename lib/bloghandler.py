#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2

#In /data/navigation/ the all structural data of the site is stored. This includes navigation bars, main sections of the site 
#and everything which isn't generated by users.
from data.navigation import navigation
try:
    from data.security import security
    secret = security.SECRET_WORD
except:
    secret = "As34gHkkflk5"

import db.user as db_user

#adding api to all pages
import json

#hasing
import hmac

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


#--------------------------------------------------------------------


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class BlogHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        if self.user:
            name = self.user.name
        else:
            name = None
        self.write(self.render_str(template,
                                 HeaderMenu = navigation.HeaderMenu,
                                 loginname = name,
                                 style = '',
                                 **kw))

    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and db_user.User.by_id(int(uid))
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'
