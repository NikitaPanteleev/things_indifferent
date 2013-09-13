from google.appengine.ext import db
from lib.bloghandler import render_str


def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.ReferenceProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    permanent_link = db.StringProperty()
    last_modified = db.DateTimeProperty(auto_now = True)
    number_of_comments = db.IntegerProperty(default = 0)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = blog_key())
        
    def render(self):
        return render_str("post.html", p = self)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt)}
        return d
