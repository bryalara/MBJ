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
"""
def ActuallySearching(property):
    user = users.get_current_user()
    profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
    profile = profile_key.get()

    if profile:
        return profile(property)
        self.redirect('/results_page')"""

class SearchPage(webapp2.RequestHandler):
    def get(self):
        name = ""
        template = env.get_template('search.html')
        my_vars = {
            'name': name
        }
        self.response.out.write(template.render(my_vars))
    #this method needs to have a search bar in every page -> done in html file
    #once you press enter, will redirect to the search.html -> done in html files
    def post(self):
        #logging.info("@@@@@@ in post")
        name = self.request.get('name')
        user = users.get_current_user()
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()

        query = profile.query()
        result_list = query.fetch()
        #logging.info("@@@@@@@@#####" + str(result_list))
        template = env.get_template('search.html')
        my_vars = {
            'result_list': result_list
        }
        self.response.out.write(template.render(my_vars))

class ResultsPage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('results.html')
        my_vars = {
            'interesting': interesting
        }
        self.response.out.write(template.render())

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
        cur_user = users.get_current_user()
        log_url = ''
        if cur_user:
            log_url = users.create_logout_url('/')
        else:
            log_url = users.create_login_url('/')

        template = env.get_template('mainpage.html')
        self.response.out.write(template.render())


app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/make_profile', MakeProfile),
    ('/make_comment', MakeComment),
    ('/main_page', MainPage),
    ('/search_page', SearchPage),
    ('results_page', ResultsPage)
], debug=True)
