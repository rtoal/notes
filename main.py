import webapp2
import jinja2
from google.appengine.api import users
from models.note import Note

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('main.html')
        self.response.write(template.render())

class NoteHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = env.get_template('note_entry.html')
            self.response.write(template.render({
                'nickname' : user.nickname(),
                'logout_url': users.create_logout_url('/')}))
        else:
            self.response.write('Please <a href="%s">log in with Google first</a>' %
                users.create_login_url('/notes'))
    def post(self):
        content = self.request.get('note')
        user = users.get_current_user()
        if user:
            note = Note(user_id=user.user_id(), content=content).put()
            self.response.write('Thank you')
        else:
            self.response.write('Please <a href="%s">log in with Google first</a>' %
                users.create_login_url('/notes'))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/notes', NoteHandler),
], debug=True)
