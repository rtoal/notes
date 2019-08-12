import webapp2
import jinja2
from google.appengine.api import users
from models import Note

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        notes = Note.query().order(-Note.timestamp).fetch(limit=20)
        user = users.get_current_user()
        logout_url = users.create_logout_url('/') if user else None
        template = jinja_env.get_template('main.html')
        self.response.write(template.render({
            'notes': notes,
            'nickname' : user.nickname() if user else None,
            'logout_url': logout_url }))

class NoteHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_env.get_template('note_entry.html')
        self.response.write(template.render({
            'nickname' : user.nickname(),
            'logout_url': users.create_logout_url('/')}))
    def post(self):
        note = self.request.get('note')
        user = users.get_current_user()
        Note(user_id=user.user_id(), content=note).put()
        self.redirect('/')

class MostRecentNoteHandler(webapp2.RequestHandler):
    def get(self):
        note = Note.query().order(-Note.timestamp).get()
        self.response.headers['Content-Type'] = 'text-plain'
        self.response.write(str(note.timestamp if note else ''))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/notes', NoteHandler),
    ('/most-recent-note', MostRecentNoteHandler),
], debug=True)
