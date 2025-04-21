from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class ChineseWord(db.Model):
    __tablename__ = 'chinese_word'
    id = db.Column(db.Integer, primary_key=True)
    chinese = db.Column(db.String(50), nullable=False)
    pinyin = db.Column(db.String(100))
    english = db.Column(db.String(100))
    part_of_speech = db.Column(db.String(50))

class CustomWord(db.Model):
    __tablename__ = 'custom_word'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    user = db.relationship('User', back_populates='custom_words')
    
class KnownWord(db.Model):
    __tablename__ = 'known_word'
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('chinese_word.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    word = db.relationship('ChineseWord', backref='known_by')
    user = db.relationship('User', back_populates='known_words')

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
    custom_words = db.relationship('CustomWord', back_populates='user') 
    known_words = db.relationship('KnownWord', back_populates='user')  # ✅ match here

    
