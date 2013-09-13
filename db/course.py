#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from google.appengine.ext import db
from lib.bloghandler import render_str
from db.user import User

from collections import namedtuple

from random import random


def course_key(name = 'default'):
    return db.Key.from_path('courses', name)
def task_key(name = 'default'):
    return db.Key.from_path('tasks', name)




class Task (db.Model):
    title = db.StringProperty(required = True)
    description = db.TextProperty()
    author = db.ReferenceProperty(User, required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now = True)
    privacy = db.BooleanProperty(default = True)   #true - only author of the task
                                                   #False - all can see this post
    
    """
    str  - desription of mini units                  -
    int  - difficulty of mini units:                 1 - normal, 2 - difficult 
    int  - expected time of completing of each unit: in mins
    int  - real time of completing each unit:        in mins
    int - condition                                  10 - active
                                                     5  - frozen
                                                     1  - done
                                                     0  - failed

    """
    lifearea = db.StringProperty(default = None)
    difficulty = db.IntegerProperty(default=1)
    expected_time = db.IntegerProperty(default=15)
    real_time = db.IntegerProperty(default=15)
    condition = db.IntegerProperty(default=10)
    repeat =  db.IntegerProperty(default=0)
    was_failed = 0
    exp = db.IntegerProperty(default=0)
    
    def gained_experience(self):
        exp = self.real_time*self.difficulty*10
        #bonus for correct planning
        try:
            time_bonus = (self.expected_time - self.real_time)/(5+self.real_time)
            if time_bonus > 0.5: 
                time_bonus=0.5
            elif time_bonus< -0.25: 
                time_bonus=-0.25
        except: 
            time_bonus=0
        #bonus for repeat
        repeat_bonus = random()*self.repeat/10
        if repeat_bonus >4: 
            repeat_bonus=4
        elif repeat_bonus <0.1: 
            repeat_bonus = 0.1
        #bonus for resuming to task
        failed_bonus = self.was_failed
        if failed_bonus >4: 
            failed_bonus=4
        exp = exp*(1+time_bonus)*(1+repeat_bonus)*(1+failed_bonus)
        return int(exp)
       

    def display_privacy(self):
        if self.privacy == True:
            return """<span class="glyphicon glyphicon-eye-close"></span> <i> It's visible only to you </i>"""
        else:
            return """<span class="glyphicon glyphicon-eye-open"> </span><i> It's visible to all</i>"""

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = task_key())
    
    def render(self):
        return render_str("task.html", c = self)

    def as_dict(self):
        d = {'title': self.title,
             'description': self.description,
             }
        return d
