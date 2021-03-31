from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #foriegn key references other db models for data
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one to many relationship tags db object with id from user who created it


class User(db.Model, UserMixin): #Only for user
    #clolumns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # adds note id - all notes that user owns/created - capital leter because references name of class

