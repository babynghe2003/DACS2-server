from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    avatar = db.Column(db.String(250),default='user.png')
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.String(80), nullable=False, default="user")

    topics = db.relationship("Topics", backref='users', lazy=True)
    votes = db.relationship("VoteTopic", backref='users', lazy=True)
    comments = db.relationship('Comment', backref='users', lazy=True)
    replies = db.relationship('Reply', backref='users', lazy=True)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


class Topics(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey("users.id"), nullable=False)
    tittle = db.Column(db.String(250), nullable=False)
    body = db.Column(db.JSON, nullable=False)

    votes = db.relationship('VoteTopic', backref='topics', lazy=True)
    comments = db.relationship('Comment', backref='topics', lazy=True)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


class VoteTopic(db.Model):
    id = db.Column(db.String(250), primary_key=True);
    user_id = db.Column(db.String(250), db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.String(250), db.ForeignKey('topics.id'), nullable=False)

    vote_action = db.Column(db.Integer, nullable=False)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


class Comment(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey('users.id'), nullable=False)
    topics_id = db.Column(db.String(250), db.ForeignKey('topics.id'), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    replies = db.relationship('Reply', backref='comment', lazy=True)
    votes = db.relationship('VoteComment', backref='comment', lazy=True)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


class VoteComment(db.Model):
    id = db.Column(db.String(250), primary_key=True);
    user_id = db.Column(db.String(250), db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.String(250), db.ForeignKey('comment.id'), nullable=False)

    vote_action = db.Column(db.Integer, nullable=False)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


class Reply(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.String(250), db.ForeignKey('comment.id'), nullable=False)

    content = db.Column(db.Text(), nullable=False)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())
