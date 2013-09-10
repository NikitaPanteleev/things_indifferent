from google.appengine.ext import db
from lib.bloghandler import render_str


def comment_key(name = 'default'):
    return db.Key.from_path('blog_comments', name)

class Comment(db.Model):
    content = db.TextProperty(required = True)
    author = db.ReferenceProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    #post_id = db.ReferenceProperty(required = True)

    def render(self):
        return render_str("comment.html", c = self)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             }
        return d