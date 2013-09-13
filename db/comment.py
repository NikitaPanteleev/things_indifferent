from google.appengine.ext import db
from lib.bloghandler import render_str
from db.post import Post
from db.user import User


def comment_key(name = 'default'):
    return db.Key.from_path('blog_comments', name)

class Comment(db.Model):
    content = db.TextProperty(required = True)
    author = db.ReferenceProperty(User,required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    post = db.ReferenceProperty(Post,required = True)
    
    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = comment_key())

    def render(self):
        return render_str("comment.html", c = self)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             }
        return d