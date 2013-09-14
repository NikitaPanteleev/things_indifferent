#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
import hmac
import random
from string import letters

from google.appengine.ext import db

#user stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    registered = db.DateTimeProperty(auto_now_add = True)
    total_exp = db.IntegerProperty(default=0)
    #a kind of achievment
    mushrooms = db.ListProperty(int,default=[0])
    time_spent = db.IntegerProperty(default = 0)

    def render(self):
        profile_str = "/community/%s/profile"%(self.name)
        blog_str = "/community/%s/blog"%(self.name)
        html = """<a href = "%s"><span class="glyphicon glyphicon-user"> </span></a>
                    <a href = "%s">%s</a>"""%(profile_str,blog_str,self.name)
        return html

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = users_key())
   
    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return cls(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u