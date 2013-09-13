#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db
from lib.safe_input import input_to_safe_html
from lib.safe_input import input_to_extended_safe_html
import lib.bloghandler as bloghandler
import db.post as db_post
import db.user as db_user
import db.comment as db_comment

SUBJECTLEN = 40
class BlogFront(bloghandler.BlogHandler):
    def get(self, user):
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
                self.render ('base.html',error = "There is no such user.")

class NewPost(bloghandler.BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html", title = "Things indifferrent",)
        else:
            self.redirect("/login")
    


    def post(self):
        if not self.user:
            self.redirect('/login')

        subject = self.request.get('subject') [:SUBJECTLEN]
        content = self.request.get('content')

        if subject and content:
            subject = input_to_safe_html(subject)
            content = input_to_extended_safe_html(content)
            p = db_post.Post(parent = db_post.blog_key(), subject = subject, content = content, 
                             author = self.user)
            p.put()
            p.permanent_link = '/community/%s/post/%s' % (str(self.user.name),str(p.key().id()))
            p.put() 
            #The weak part of the code. DB is touching twice here.
            #
            self.redirect(p.permanent_link)
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error_blog=error,
                        title = "Things indifferrent",)

class PostPage(bloghandler.BlogHandler):
    def get(self, OP, post_id):
        OP = db_user.User.by_name(OP)
        post = db_post.Post.by_id(int(post_id))
        if (not post or not OP):
            self.render ("base.html", error = "There is no such user or post",
                                  title = "Things indifferrent",
                        )
            return
        if self.format == 'html':
            #-----------------------------------
            comments = db_comment.Comment.all().filter("post = ", post.key()).order('created')
            #-----------------------------------
            self.render("permalink.html", p = post, comments = comments, title = "Things indifferrent")
        else:
            return self.render_json(post.as_dict())
            
    def post(self,OP,post_id):
        OP = db_user.User.by_name(OP)
        post = db_post.Post.by_id(int(post_id))

        if not self.user:
            self.redirect('/login')
            return


        comment = self.request.get('comment')
        if comment:
            comment = input_to_extended_safe_html(comment)
            
            c = db_comment.Comment(parent = db_comment.comment_key(), content = comment, 
                             author = self.user.key(), post = post.key())
            c.put()
            post.number_of_comments+=1
            post.put()
            self.redirect(post.permanent_link)
        else:
            error = "No content!"
            self.render("permalink.html", p = post, comments = comments, title = "Things indifferrent",
                        error = "Content please!")