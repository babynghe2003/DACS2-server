from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime
import uuid

db = SQLAlchemy()


@dataclass
class Users(db.Model):

    id: str
    username: str
    email: str
    role: str
    number: str
    address: str
    create_at: datetime
    topics: object

    id = db.Column(db.String(250), primary_key=True)
    avatar = db.Column(db.String(250), default='user.png')
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    address = db.Column(db.String(250))
    number = db.Column(db.String(11))
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.String(80), nullable=False, default="user")

    topics = db.relationship("Topics", backref='users', lazy=True)
    votes = db.relationship("VoteTopic", backref='users', lazy=True)
    comments = db.relationship('Comments', backref='users', lazy=True)
    replies = db.relationship('Reply', backref='users', lazy=True)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


@dataclass
class Topics(db.Model):

    id: str
    tittle: str
    body: str
    create_at: str

    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey(
        "users.id"), nullable=False)
    tittle = db.Column(db.String(250), nullable=False)
    body = db.Column(db.JSON, nullable=False)

    user = db.relationship('Users', backref='Topics', viewonly=True, lazy=True)
    votes = db.relationship('VoteTopic', backref='topics', lazy=True)
    comments = db.relationship('Comments', backref='topics', lazy=True)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


@dataclass
class VoteTopic(db.Model):

    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey(
        'users.id'), nullable=False)
    topic_id = db.Column(db.String(250), db.ForeignKey(
        'topics.id'), nullable=False)

    vote_action = db.Column(db.Integer, nullable=False)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


@dataclass
class Comments(db.Model):
    id: str
    user_id: str
    content: str
    user: object
    create_at: datetime

    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey(
        'users.id'), nullable=False)
    topics_id = db.Column(db.String(250), db.ForeignKey(
        'topics.id'), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    user = db.relationship('Users', backref='Comments',
                           viewonly=True, lazy=True)

    replies = db.relationship('Reply', backref='comments', lazy=True)
    votes = db.relationship('VoteComment', backref='comments', lazy=True)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


@dataclass
class VoteComment(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey(
        'users.id'), nullable=False)
    comment_id = db.Column(db.String(250), db.ForeignKey(
        'comments.id'), nullable=False)

    vote_action = db.Column(db.Integer, nullable=False)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


@dataclass
class Reply(db.Model):
    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey(
        'users.id'), nullable=False)
    comment_id = db.Column(db.String(250), db.ForeignKey(
        'comments.id'), nullable=False)

    content = db.Column(db.Text(), nullable=False)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())


@dataclass
class Report(db.Model):

    id = db.Column(db.String(250), primary_key=True)
    user_id = db.Column(db.String(250), db.ForeignKey(
        'users.id'), nullable=False)
    topic_id = db.Column(db.String(250), db.ForeignKey(
        'topics.id'), nullable=False)

    create_at = db.Column(db.DateTime(), default=datetime.now())
    update_at = db.Column(db.DateTime(), onupdate=datetime.now())
