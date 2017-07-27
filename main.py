import webapp2
import logging
import urllib #allows you to make communcation to the outside world (to call the https)
import urllib2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import datetime
import os
import binascii

env=jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.dirname(__file__)))

class Profile(ndb.Model):
    name = ndb.StringProperty()
    education = ndb.StringProperty()
    objective = ndb.StringProperty()
    career = ndb.StringProperty()
    pic = ndb.BlobProperty()
    #username is the key to refer to a specific profiletop

class Comment(ndb.Model):
    name= ndb.StringProperty()
    comment = ndb.StringProperty()
    profile_key = ndb.KeyProperty(Profile)
    created_at = ndb.DateTimeProperty(auto_now=True)

class LoginPage(webapp2.RequestHandler):
    def get(self):
        cur_user = users.get_current_user()
        log_url = ''
        if cur_user:
            log_url = users.create_logout_url('/')
        else:
            log_url = users.create_login_url('/main_page')

        template = env.get_template('login.html')
        my_vars = {
            'user': cur_user,
            'log_url': log_url,
        }
        self.response.out.write(template.render(my_vars))

class SearchPage(webapp2.RequestHandler):
    def get(self):
        name = ""
        user = users.get_current_user()
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()
        log_url = users.create_logout_url('/')
        template = env.get_template('search.html')
        my_vars = {
            'name': name,
            'log_url': log_url,
            'profile': profile
        }
        self.response.out.write(template.render(my_vars))
    #this method needs to have a search bar in every page -> done in html file
    #once you press enter, will redirect to the search.html -> done in html files
    def post(self):
        #logging.info("@@@@@@ in post")
        name = self.request.get('name')
        user = users.get_current_user()
        log_url = users.create_logout_url('/')
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()
        query = profile.query()
        result_list = query.fetch()
        #logging.info("@@@@@@@@#####" + str(result_list))
        if profile and profile.pic: #green part is the url. nect part is the data for the iamge.
            #binascii is a library. b2a converts the binary string into a base 64 string. stikcing onto url with the profile pic data
            pic = "data:image;base64," + binascii.b2a_base64(profile.pic)
        else:
            pic = "../resources/handshake.jpg"
        template = env.get_template('search.html')
        my_vars = {
            'result_list': result_list,
            'log_url': log_url,
            'pic': pic
        }
        self.response.out.write(template.render(my_vars)) #make the answers show up on results.html

class MakeProfile(webapp2.RequestHandler):
    def get(self):
        #name = Profile.get('name')
        name = ""
        education = ""
        objective = ""
        career = ""
        log_url = users.create_logout_url('/')
        template = env.get_template('makeprofile.html')
        my_vars = {
            'name': name,
            'education': education,
            'objective': objective,
            'career': career,
            'log_url': log_url,
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
                career = self.request.get('career'),
                pic = self.request.get('pic'))
        profile.key = profile_key
        profile.put()
        self.redirect('/profile_page')

def timedelta_to_microtime(td):
    return td.microseconds + (td.seconds + td.days * 86400) * 1000000

def comment_sort_function(a, b):
    ca = a.created_at
    if not ca:
        return 1
    cb = b.created_at
    if not cb:
        return -1

    return timedelta_to_microtime(a.created_at - b.created_at)

class MakeComment(webapp2.RequestHandler):
    def get(self):
        name = ""
        comment = ""
        created_at = ""

        query = Comment.query()
        comment_list = query.fetch()

        user = users.get_current_user()
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()

        comment_list.sort(comment_sort_function)
        log_url = users.create_logout_url('/')
        template = env.get_template('comment.html')
        my_vars = {
            'name': name,
            'comment': comment,
            'comment_list': comment_list,
            'log_url': log_url,
            'profile': profile
        }
        self.response.out.write(template.render(my_vars))

    def post(self):
        user = users.get_current_user()
        comment_key = ndb.Key('Comment', self.request.get('comment')+str(datetime.datetime.now()))
        comment = comment_key.get()

        profile_key = ndb.Key('Profile', user.nickname())
        profile = profile_key.get()

        if not comment:
            comment = Comment(
                name = self.request.get('name'),
                comment = self.request.get('comment'),
                created_at = datetime.datetime.now(),
                profile_key = profile.key)
        comment.key = comment_key
        comment.put()
        self.redirect('/make_comment')

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()
        log_url = users.create_logout_url('/')
        template = env.get_template('mainpage.html')
        my_vars = {
            'profile': profile,
            'log_url': log_url
        }
        self.response.out.write(template.render(my_vars))

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        if self.request.get("id"):
            name_key = ndb.Key(urlsafe=self.request.get("id"))
            profile = name_key.get()
        else:
            user = users.get_current_user()
            profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
            profile = profile_key.get()
        log_url = users.create_logout_url('/')
        if profile and profile.pic: #green part is the url. nect part is the data for the iamge.
            #binascii is a library. b2a converts the binary string into a base 64 string. stikcing onto url with the profile pic data
            pic = "data:image;base64," + binascii.b2a_base64(profile.pic)
        else:
            pic = "../resources/handshake.jpg"

        template = env.get_template('profile.html')
        my_vars = {
            'profile': profile,
            'pic': pic,
            'log_url': log_url
        }
        self.response.out.write(template.render(my_vars))

class About(webapp2.RequestHandler):
    def get(self):
        template= env.get_template('about.html')
        self.response.out.write(template.render())

class Women(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()
        template= env.get_template('women_discussion.html')
        my_vars = {
            'profile': profile
        }
        self.response.out.write(template.render(my_vars))

class CompSci(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        profile_key = ndb.Key('Profile', user.nickname()) #.nickname returns the email
        profile = profile_key.get()
        template= env.get_template('cs_discussion.html')
        my_vars = {
            'profile': profile
        }
        self.response.out.write(template.render(my_vars))


app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/make_profile', MakeProfile),
    ('/make_comment', MakeComment),
    ('/main_page', MainPage),
    ('/search_page', SearchPage),
    ('/profile_page', ProfilePage),
    ('/about', About),
    ('/women', Women),
    ('/cs', CompSci)
], debug=True)
