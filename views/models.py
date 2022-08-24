from datetime import date
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(500))
    user_name = db.Column(db.String(150),nullable=False, unique=True)
    
    gender = db.Column(db.String(150))

    name = db.Column(db.String(150), nullable=True, default='None')
    bio = db.Column(db.Text(150), nullable=True, default='None')
    profile_pic = db.Column(db.String(100000), default='Default/Default.jpeg')

    date = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='poster')
   
    admin = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='user')
    

    

    def __repr__(self) :
        return '<Name %r>' %self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(10000),nullable=True)
    edited=db.Column(db.Boolean, default=False)
    
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes= db.relationship('Post_like', backref='like')
    comments = db.relationship('Comment', backref='post')
    
    img_name = db.Column(db.String(100000), unique=True)
    mimetype = db.Column(db.Text, nullable=True)
    
class Admin(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email= db.Column(db.Integer)
    password = db.Column(db.String(500),nullable=True)
    name = db.Column(db.String(150),nullable=True)

class Post_like(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    post_id =db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    
class Comment (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    text = db.Column(db.String(10000),nullable=False)
    edited=db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    