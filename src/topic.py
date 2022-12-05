import uuid
from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from src.models import Users, db, Topics, Comments, VoteTopic, VoteComment
from sqlalchemy import func, distinct
import json

topics = Blueprint("topics", __name__, url_prefix="/api/v1/topics")


@topics.post('/create-topic')
@jwt_required()
def create_topics():
    tittle = request.json['title']
    body = request.json['body']
    user_id = get_jwt_identity()
    id = uuid.uuid4()

    # print(request.json)

    topic = Topics(id=id, tittle=tittle, body=body, user_id=user_id)
    db.session.add(topic)
    db.session.commit()

    return jsonify({
        'message': "topics created",
        'topics': {
            'tittle': tittle, "id": id
        }

    }), HTTP_201_CREATED


@topics.patch('/update-topic/<id>')
@jwt_required()
def update_topic(id):
    topic = Topics.query.filter_by(id=id).first()

    for key in request.json:
        setattr(topic, key, request.json[key])

    db.session.commit()

    return jsonify({
        "update": topic.id,
        "tittle": topic.tittle,
        "new": topic.body
    }), HTTP_200_OK


@topics.get('/all-topics')
@jwt_required()
def all_topics():
    topicsList = Topics.query.all()
    topics = []
    for topic in topicsList:
        topics.append({
            "id": topic.id,
            "tittle": topic.tittle,
            "body": topic.body,
            "author": topic.user.username,
            "author_id": topic.user.id,
            "create_at": topic.create_at,
            "likes": len([i for i in topic.votes if i.vote_action == 1]) - len([i for i in topic.votes if i.vote_action == 2]),
            "answers": len(topic.comments)
        })
    # print(topicsList.user.username)
    return jsonify({
        "data": topics
    }), HTTP_200_OK


@topics.post('/comment')
@jwt_required()
def comment():
    user_id = get_jwt_identity()
    topic_id = request.json['topic_id']
    content = request.json['content']
    id = uuid.uuid4()
    cmt = Comments(id=id, user_id=user_id, topics_id=topic_id, content=content)
    db.session.add(cmt)
    db.session.commit()

    return jsonify({
        "message": "Comment success",
        "comment": {
            "id": id,
            "content": content
        }
    }), HTTP_200_OK


@topics.post('/vote')
@jwt_required()
def vote_topic():
    user_id = get_jwt_identity()
    topic_id = request.json['topic_id']
    vote_action = request.json['vote_action']
    id = uuid.uuid4()

    vote = VoteTopic(id=id, user_id=user_id,
                     topic_id=topic_id, vote_action=vote_action)
    db.session.add(vote)
    db.session.commit()

    return jsonify({
        "message": "Comment success",
        "comment": {
            "id": id,
            "action": vote_action
        }
    }), HTTP_200_OK


@topics.post('/vote-comment')
@jwt_required()
def vote_comment():
    user_id = get_jwt_identity()
    comment_id = request.json['comment_id']
    vote_action = request.json['vote_action']
    id = uuid.uuid4()

    vote = VoteComment(id=id, user_id=user_id,
                       comment_id=comment_id, vote_action=vote_action)
    db.session.add(vote)
    db.session.commit()

    return jsonify({
        "message": "Vote success",
        "comment": {
            "id": id,
            "action": vote_action
        }
    }), HTTP_200_OK


@topics.get('/my-topics')
@jwt_required()
def my_topics():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()
    res = []
    for topic in user.topics:
        res.append({
            "id": topic.id,
            "tittle": topic.tittle,
            "body": topic.body,
            "author": topic.user.username,
            "author_id": topic.user.id,
            "create_at": topic.create_at,
            "likes": len([i for i in topic.votes if i.vote_action == 1]) - len([i for i in topic.votes if i.vote_action == 2]),
            "answers": len(topic.comments)
        })
    return jsonify({
        "data": res
    }), HTTP_200_OK


@topics.get('/topic/<id>')
@jwt_required()
def topic(id):
    topic = Topics.query.filter_by(id=id).first()
    comments = []
    for comment in topic.comments:
        comments.append({
            "id": comment.id,
            "user_id": comment.user_id,
            "content": comment.content,
            "user": comment.user,
            "create_at": comment.create_at,
            "likes": len([i for i in comment.votes if i.vote_action == 1]) - len([i for i in comment.votes if i.vote_action == 2])

        })
    return jsonify({
        'topic': {
            "id": id,
            "title": topic.tittle,
            "body": topic.body,
            "user": topic.user,
            "create_at": topic.create_at,
            "likes": len([i for i in topic.votes if i.vote_action == 1]) - len([i for i in topic.votes if i.vote_action == 2]),
            "answers": len(topic.comments)
        },
        'comments': comments
    }
    ), HTTP_200_OK


@topics.delete('/delete-topic/<id>')
@jwt_required()
def delete_user(id):
    user_id = get_jwt_identity()
    topic = Topics.query.filter_by(id=id).first()
    if (topic.user_id != user_id):
        return jsonify({
            "message": "Not allowed"
        }), HTTP_405_METHOD_NOT_ALLOWED
    # Users.query.filter_by(id=id).delete()
    print(id)
    db.session.query(Topics).filter(Topics.id == id).delete()
    db.session.commit()
    return jsonify({
        'message': 'Delete success',
    }), HTTP_200_OK
