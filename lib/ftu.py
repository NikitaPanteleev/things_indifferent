#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db
from random import randint
from lib.safe_input import input_to_safe_html
from lib.safe_input import input_to_extended_safe_html

import lib.bloghandler as bloghandler
import db.user as db_user
import db.course as db_course
from data.ftu import ftu as ftu_struct

SUBJECTLEN = 40


class TaskFront(bloghandler.BlogHandler):
    def get(self, user):
        condition = self.request.get("condition")
        if not condition:
            condition = -1
        else:
            condition = int(condition)
        if user == "all":
            tasks = db_course.Task.all().filter('privacy = ', False).order('-modified')
            if self.format == 'html':
                self.render('fronttask.html', tasks = tasks, title = "All tasks",)
            else:
                return self.render_json([t.as_dict() for t in tasks])
        else:
            if not self.user:
                self.redirect('/ftu/intro/')
                return
            user = db_user.User.by_name (user)
            if user:
                if user.name == self.user.name:
                    tasks = db_course.Task.all().filter('author = ',user.key())
                else:
                    tasks = db_course.Task.all().filter('author = ',user.key()).\
                    filter('privacy = ', False)
                if condition ==-1:
                    tasks = tasks.order('-modified')
                else:
                    tasks = tasks.filter('condition = ', condition).order('-modified')
                                
                if self.format == 'html':
                    self.render('fronttask.html', tasks = tasks,title = "%s' tasks"%user.name)
                else:
                    return self.render_json([t.as_dict() for t in tasks])
            else:
                self.render ('base.html',error_text = "There is no such user.")

class NewTask(bloghandler.BlogHandler):
    def get(self):

        if self.user:
            self.render("newtask.html", title = "Things indifferrent", lifearea = ftu_struct.LifeArea)
        else:
            self.redirect("/login")
    
    def post(self):
        if not self.user:
            self.redirect('/login')

        ctitle = self.request.get('ctitle') [:SUBJECTLEN]
        cdesc = self.request.get('cdesc')
        cprivacy = self.request.get('cprivacy')
        clifearea = self.request.get('clifearea')
        cdiff = self.request.get('cdiff')
        cexptime = self.request.get('cexptime')
        cchosentime = self.request.get('cchosentime')
       
        if ctitle and (cexptime or cchosentime):
            if cexptime:
                exptime = int(cexptime)
            else:
                exptime = int(cchosentime)
            subject = input_to_safe_html(ctitle)
            cdesc = input_to_extended_safe_html(cdesc)
            cprivacy = bool(int(cprivacy))
            c = db_course.Task(parent = db_course.task_key(), title = ctitle, description = cdesc, 
                             author = self.user, privacy = cprivacy, 
                             lifearea = clifearea, difficulty = int(cdiff),
                             expected_time = exptime, real_time = exptime,
                             condition = 10)

            c.put()
           
            self.redirect("/ftu/%s/tasks?condition=10"%(self.user.name) )

        else:
            self.render("newtask.html", title = "Things indifferrent",lifearea = ftu_struct.LifeArea,
                         error = "Fill all fields, please.", 
                         ctitle = ctitle,
                         cdesc = cdesc,
                         )


class TaskPage(bloghandler.BlogHandler):
    def get(self, task_id):
        task = db_course.Task.by_id(int(task_id))
       
        if not task:
            self.render ("base.html", error = "There is no such task.")
            return
            
        if self.format == 'html':
            self.render("tasklink.html", c = task, title = "Things indifferrent")
        else:
            self.render_json(post.as_dict())

class TaskIntro(bloghandler.BlogHandler):
    def get(self):
       self.render("taskintro.html", title = "Introduction to FTU")

class TaskEdit(bloghandler.BlogHandler):
    def post(self):
        if not self.user:
            self.redirect("/login")
            return
        condition = self.request.get("tcondition")  #finish
                                                    #freeze
                                                    #fail
        treal = self.request.get('treal')
        
        if condition:
            (condition, task_id) = condition.split("|")
            task_id = int(task_id)
        
            task = db_course.Task.by_id(task_id)
            if self.user.name != task.author.name:
                self.render('base.html', error = "You can update only your tasks!",
                                     title = "Error",)
                return


            if condition == "finish" and treal:
                #expirience
                task.condition = 1
                task.real_time = int(treal)
                
                exp = task.gained_experience()
                task.exp+=exp
                
                task.repeat+=1

                task.put()
                #------------
                #mushroom hunting
                mushroom = randint(1,20)
                if mushroom == 13:
                    self.user.mushrooms.append(1)
                self.user.total_exp += exp
                self.user.time_spent +=task.real_time
                print task.real_time
                print self.user.time_spent
                print "\n\n\n"
                self.user.put()
            elif condition == "freeze":
                task.condition = 5
                task.put()
            elif condition == "fail":
                task.condition = 0
                task.put()
            self.redirect ("/ftu/%s/tasks?condition=10"%(self.user.name))
            return
        tresume = self.request.get('tresume')
        if tresume:
            task = db_course.Task.by_id(int(tresume))
            if task:
                task.condition = 10
                task.was_failed+=1
                task.put()
            self.redirect ("/ftu/%s/tasks?condition=10"%(self.user.name))    
            return
        trepeat = self.request.get('trepeat')
        if trepeat:
            task = db_course.Task.by_id(int(trepeat))
            if task:
                task.condition = 10
                task.repeat+=1
                task.put()
            self.redirect ("/ftu/%s/tasks?condition=10"%(self.user.name))    
            return
        self.render('base.html', error = "Error while updating task.",
                                     title = "Error",)
        

