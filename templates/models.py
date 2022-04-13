from datetime import timezone
from email.policy import default
from enum import unique
from sqlalchemy import PrimaryKeyConstraint
from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
     id = db.Column(db.Integer,Primary_key=True)
     data =db.Column(db.String(10000))
     date= db.Column(db.DateTime(timezone=True),default=func.now())
     user_id =db.Column(db.Integer,db.models.ForeignKey('user.id'))
      

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,Primary_key=True)
    email = db.Column(db.String(150), unique =True)
    password=db.Column(db.String(150))
    user_name=db.Column(db.String(150), unique=True)
    notes = db.relationship('Note')
    
    

   
