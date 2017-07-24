import webapp2
import logging
import urllib #allows you to make communcation to the outside world (to call the https)
import urllib2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2

env=jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        cur_user = users.get_current_user()
        log_url = ''
        if cur_user:
            log_url = users.create_logout_url('/')
        else:
            log_url = users.create_login_url('/')

        my_vars = {
            'user': cur_user,
            'log_url': log_url,
        }


class Comment(ndb.Model):
    name= ndb.StringProperty()
    comment = ndb.StringProperty

class MakeComment(webapp2.RequestHandler):
    def post(self):
        comment_key = ndb.Key("Comment", self.request.get("comment"))
        comment= comment_key.get()
        if not comment:
            comment = Comment(
            name= self.request.get("name"),
            comment= self.request.get("comment")
            )
            comment.key= comment_key
            comment.put()
        self.redirect("/")


class Profile(ndb.Model):
    def get(self):
        #username is the key to refer to a specific profilekop

class MakeProfile(webapp2.RequestHandler):
    def post(self):



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/make_profile', MakeProfile),
    ('/make_comment', MakeComment),
], debug=True)
