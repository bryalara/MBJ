import webapp2
import logging
import urllib #allows you to make communcation to the outside world (to call the https)
import urllib2
import jinja2

env=jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):



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

class MakeProfile(webapp2.RequestHandler):
    def post(self):



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/make_profile', MakeProfile),
    ('/make_comment', MakeComment),
], debug=True)
