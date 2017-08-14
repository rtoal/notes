import webapp2
import jinja2
from google.appengine.api import users
from models.note import Note

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        notes = Note.query().order(-Note.timestamp).fetch(limit=20)
        template = env.get_template('main.html')
        self.response.write(template.render({ 'notes': notes }))

class NoteHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('note_entry.html')
        self.response.write(template.render({
            'nickname' : user.nickname(),
            'logout_url': users.create_logout_url('/')}))
    def post(self):
        content = self.request.get('note')
        user = users.get_current_user()
        note = Note(user_id=user.user_id(), content=content).put()
        self.response.write('Thank you')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/notes', NoteHandler),
], debug=True)
