from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

#set up variables
login_manager= LoginManager()
ma= Marshmallow()
db= SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#this clas is to create the ability for people to log in
class User(db.Model, UserMixin):
    id= db.Column(db.String, primary_key=True)
    first_name= db.Column(db.String(150), nullable=True, default='')
    last_name= db.Column(db.String(150), nullable=True, default='')
    email= db.Column(db.String(150), nullable=False)
    password= db.Column(db.String, nullable=True, default='')
    g_auth_verify= db.Column(db.Boolean, default=False)
    token= db.Column(db.String, default='', unique=True)
    date_created= db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __init__(self, email, first_name= '', last_name= '', password= '', token= '', g_auth_verify=False):
        self.id= self.set_id()
        self.first_name= first_name
        self.last_name=last_name
        self.password= self.set_password(password)
        self.email= email
        self.token= self.set_token(10)
        self.g_auth_verify= g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash= generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created.'

#this class is to add book to the library database
class Inventory(db.Model):
    id= db.Column(db.String,primary_key=True)
    author= db.Column(db.String(200))
    title= db.Column(db.String(200))
    genre= db.Column(db.String(50))
    isbn= db.Column(db.String)#abook isbn does not change thus is string
    copies= db.Column(db.Numeric)
    user_token= db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, author, title, genre, isbn, copies, user_token, id= ''):
        self.id= self.set_id()
        self.author= author
        self.title= title
        self.genre= genre
        self.isbn= isbn
        self.copies= copies
        self.user_token= user_token

    def __repr__(self):
        return f'The following book has been added to the inventory: {self.title} id# {self.id}'

    def set_id(self):
        return (secrets.token_urlsafe())

class InvenSchema(ma.Schema):
    class Meta:
        fields = ['id', 'author', 'title', 'genre', 'isbn', 'copies']

inven_schema = InvenSchema()
invens_schema = InvenSchema(many=True)


        


