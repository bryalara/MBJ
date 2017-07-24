class MainPage(webapp2.RequestHandler):
    def get(self):



class Comment(ndb.Model):
    def get(self):

class MakeComment(webapp2.RequestHandler):
    def post(self):



class Profile(ndb.Model):
    def get(self):

class MakeProfile(webapp2.RequestHandler):
    def post(self):



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/make_profile', MakeProfile),
    ('/make_comment', MakeComment),
], debug=True)
