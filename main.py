import webapp2
import logging
import urllib #allows you to make communcation to the outside world (to call the https)
import urllib2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os

env=jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.dirname(__file__)))

class Searching(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    education = ndb.StringProperty(indexed=True)
    objective = ndb.StringProperty(indexed=True)
    career = ndb.StringProperty(indexed=True)

class Search(webapp2.RequestHandler):
    def get(self):
        search_term = self.request.get('search_term')
        if cur_user:
            query = Searching.query(
                ancestor = ndb.Key('Profile', search_term))
            results = query.fetch()

        template = env.get_template('search.html')
        my_vars = {
            'results': results,
            'search_term': search_term
        }
        self.response.out.write(template.render(my_vars))

class LoginPage(webapp2.RequestHandler):
    def get(self):
        cur_user = users.get_current_user()
        log_url = ''
        if cur_user:
            log_url = users.create_logout_url('/')
        else:
            log_url = users.create_login_url('/')

        template = env.get_template('login.html')
        my_vars = {
            'user': cur_user,
            'log_url': log_url,
        }
        self.response.out.write(template.render(my_vars))

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
    name = ndb.StringProperty(indexed=True)
    education = ndb.StringProperty(indexed=True)
    objective = ndb.StringProperty(indexed=True)
    career = ndb.StringProperty(indexed=True)
    #username is the key to refer to a specific profilekop

class MakeProfile(webapp2.RequestHandler):
    def get(self):
        #name = Profile.get('name')
        name = ""
        education = ""
        objective = ""
        career = ""

        template = env.get_template('makeprofile.html')
        my_vars = {
            'name': name,
            'education': education,
            'objective': objective,
            'career': career
        }
        self.response.out.write(template.render(my_vars))

    def post(self):
        user = users.get_current_user()
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()

        if not profile:
            profile = Profile(
                name = self.request.get('name'),
                education = self.request.get('education'),
                objective = self.request.get('objective'),
                career = self.request.get('career'))
        profile.key = profile_key
        profile.put()
        self.redirect('/make_profile')

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('mainpage.html')



app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/make_profile', MakeProfile),
    ('/make_comment', MakeComment),
    ('/main_page', MainPage),
    ('/search_page', Search)
], debug=True)
