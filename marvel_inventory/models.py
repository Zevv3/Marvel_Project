from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    """
    This class takes in information about the user gathered from the signup form, assigns the user a unique id and token,
    and formats the data to be added to a database.
    """
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    display_name = db.Column(db.String(150), nullable = False, default = '')
    password = db.Column(db.String, nullable = True)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    characters = db.relationship('Character', backref = 'owner', lazy = True)
    # comics = db.relationship('Comic', backref='owner', lazy=True)
    
    def __init__(self, email, display_name = '', first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
        # self.login = self.email, self.display_name


    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.display_name} has been added to the database!"


class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String)
    # num_comics is the number of commics they appear in
    # apicall = test.characters.all()['data']['results'][0]['comics']['available']
    num_comics = db.Column(db.Integer)
    # test.characters.all()['data']['results'][0]['stories']['available']
    num_stories = db.Column(db.Integer) 
    # test.characters.all()['data']['results'][0]['series']['available']
    num_series = db.Column(db.Integer)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, id, name, desc, num_comics, num_stories, num_series, user_token):
        self.id = id
        self.name = name
        self.desc = desc
        self.num_comics = num_comics
        self.num_series = num_series
        self.num_stories = num_stories
        self.user_token = user_token

    def __repr__(self):
        return f"{self.name} has been added to your favorites!"

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'desc', 'num_comics', 'num_stories', 'num_series']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)
