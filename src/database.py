from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid



db = SQLAlchemy()

class ReactTable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_react = db.Column(db.String(50), nullable = False)
    create_at = db.Column(db.DateTime(), default = datetime.now())
    update_at = db.Column(db.DateTime(), onupdate = datetime.now())
class Users(db.Model):
    id = db.Column(db.String(250), primary_key = True)
    username = db.Column(db.String(250), unique = True, nullable = False)
    email = db.Column(db.String(250), unique = True, nullable = False)
    topic = db.relationship("Topics",backref='users', lazy=True)
    password = db.Column(db.Text(), nullable = False)
    role = db.Column(db.String(80),nullable = False, default = "user")
    create_at = db.Column(db.DateTime(), default = datetime.now())
    update_at = db.Column(db.DateTime(), onupdate = datetime.now())
    
class Topics(db.Model):
    id = db.Column(db.String(250), primary_key = True)
    tittle = db.Column(db.String(250), nullable = False)
    body = db.Column(db.JSON, nullable = False)
    votes = db.relationship('Users', secondary=votes, lazy='subquery',
        backref=db.backref('topics', lazy=True))
    comments = db.relationship('Comment', backref = 'topics', lazy = True)
    user_id = db.Column(db.String(250),db.ForeignKey("users.id"),nullable=False)
    create_at = db.Column(db.DateTime(), default = datetime.now())
    update_at = db.Column(db.DateTime(), onupdate = datetime.now())

class ReactTopic(db.Model):
    user_id = db.Column(db.String(250), db.ForeignKey('user.id'), primary_key = True)
    topics_id = db.Column(db.String(250), db.ForeignKey('topics.id'), primary_key = True)
    type = db.Column(db.Integer, db.ForeignKey('reacttable.id'), nullable = False)
    create_at = db.Column(db.DateTime(), default = datetime.now())
    update_at = db.Column(db.DateTime(), onupdate = datetime.now())
class Comment(db.Model):
    id = db.Column(db.String(250), primary_key = True)
    user_id = db.Column(db.String(250), db.ForeignKey('user.id'))
    topics_id = db.Column(db.String(250), db.ForeignKey('topics.id'))
    content = db.Column(db.Text(),nullable = False)
    create_at = db.Column(db.DateTime(), default = datetime.now())
    update_at = db.Column(db.DateTime(), onupdate = datetime.now())
class Reply(db):
    id = db.Column(db.String(250), primary_key = True)
    user_id = user_id = db.Column(db.String(250), db.ForeignKey('user.id'), primary_key = True)
    comment_id = db.Column(db.String(250), db.ForeignKey('comment.id'), primary_key = True)
    content = db.Column(db.Text(),nullable = False)
    create_at = db.Column(db.DateTime(), default = datetime.now())
    update_at = db.Column(db.DateTime(), onupdate = datetime.now())