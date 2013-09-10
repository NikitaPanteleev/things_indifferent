#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db
from lib.safe_input import input_to_safe_html
from lib.safe_input import input_to_extanded_safe_html
import lib.bloghandler as bloghandler
import db.post as db_post
import db.user as db_user
import db.comment as db_comment

SUBJECTLEN = 40

"""
def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)
"""
class BlogFront(bloghandler.BlogHandler):
    def get(self, user):
        #self.render ('base.html',simple_text = "This is the blog of %s"%user)
        #str to instance object. Be carefull here
        if user == "all":
            posts = db_post.Post.all().order('-created')
            if self.format == 'html':
                self.render('front.html', posts = posts, title = "All posts",)
            else:
                return self.render_json([p.as_dict() for p in posts])

        else:
            user = db_user.User.by_name (user)
            if user:
                posts = db_post.Post.all().filter('author = ',user.key())
                #db.GqlQuery("select * from Customers where ID = %s" % id)
                if self.format == 'html':
                    self.render('front.html', posts = posts,title = "%s' blog"%user.name)
                else:
                    return self.render_json([p.as_dict() for p in posts])
            else:
                self.render ('base.html',error_text = "There is no such user.")

class NewPost(bloghandler.BlogHandler):
    """
        This class renders "newpost.html" template where user can input subject and content of a new post.
        If they both are presented, they are instantly encodered to safe html by means of
        input_to_safe_html() from lib.safe_input ( it replaces '<' by u'&lt' but allows some simple
        html tags). If content or subject are not presented it render "newpost.html" again.
    """
    def get(self):
        if self.user:
            self.render("newpost.html", title = "Things indifferrent",)
        else:
            self.redirect("/login")
    


    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject') [:SUBJECTLEN]
        content = self.request.get('content')

        if subject and content:
            subject = input_to_safe_html(subject)
            content = input_to_extanded_safe_html(content)
            p = db_post.Post(parent = self.user, subject = subject, content = content, 
                             author = self.user)
            p.put()
            p.permanent_link = '/community/%s/post/%s' % (str(self.user.name),str(p.key().id()))
            p.put() 
            #The weak part of the code. DB is touching twice here.
            #
            self.redirect(p.permanent_link)
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error,
                        title = "Things indifferrent",)

class PostPage(bloghandler.BlogHandler):
  
    def get(self, OP, post_id):
        OP = db_user.User.by_name(OP)
        key = db.Key.from_path('Post', int(post_id), parent=OP.key())
        post = db.get(key)
        #post = db_post.Post.all().filter("subject =","top").get()
               
        if not post:
            self.error(404)
            return
        if self.format == 'html':
            comments = db_comment.Comment.all().ancestor(post).order('-created')
            self.render("permalink.html", p = post, comments = comments, title = "Things indifferrent")
        else:
            return self.render_json(post.as_dict())
            
    def post(self,OP,post_id):
        OP = db_user.User.by_name(OP)
        key = db.Key.from_path('Post', int(post_id), parent=OP.key())
        post = db.get(key)
        
        if not self.user:
            self.redirect('/blog')

        comment = self.request.get('comment')
        comments = db_comment.Comment.all().ancestor(post).order('-created')
        if comment:
            comment = input_to_extanded_safe_html(comment)
            
            c = db_comment.Comment(parent = post, content = comment, 
                             author = self.user.key(), post = post.key())
            c.put()
            self.redirect(post.permanent_link)
        else:
            error = "No content!"
            self.render("permalink.html", p = post, comments = comments, title = "Things indifferrent",
                        error = "Content please!")