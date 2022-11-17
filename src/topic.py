import uuid
from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from src.models import Users, db, Topics, Comment, VoteTopic, VoteComment
from sqlalchemy import func, distinct
import json

topics = Blueprint("topics", __name__, url_prefix="/api/v1/topics")


@topics.post('/create-topic')
@jwt_required()
def create_topics():
    tittle = request.json['tittle']
    body = request.json['body']
    user_id = get_jwt_identity()
    id = uuid.uuid4();

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
        "tittle":topic.tittle,
        "new": topic.body
    }), HTTP_200_OK

# @topics.get('/all-topics/<page>/<rowsperpage>')
# @jwt_required()
# def all_topics(page,rowsperpage):
#     topicsList = Topics.query\
#         .join(Users, Users.id == Topics.user_id)\
#         .add_column(Users.username, Users.email, Topics.tittle, func.count(Topics.votes), Topics.comments)

@topics.post('/comment')
@jwt_required()
def comment():
    user_id = get_jwt_identity()
    topic_id = request.json['topic_id']
    content = request.json['content']
    id = uuid.uuid4()
    cmt = Comment(id = id, user_id = user_id, topics_id = topic_id, content = content)
    db.session.add(cmt)
    db.session.commit()

    return jsonify({
        "message":"Comment success",
        "comment":{
            "id":id,
            "content":content
        }
    }), HTTP_200_OK

@topics.post('/vote')
@jwt_required()
def vote_topic():
    user_id = get_jwt_identity()
    topic_id = request.json['topic_id']
    vote_action = request.json['vote_action']
    id = uuid.uuid4()

    vote = VoteTopic(id = id, user_id = user_id, topic_id = topic_id, vote_action = vote_action)
    db.session.add(vote)
    db.session.commit()

    return jsonify({
        "message": "Comment success",
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
            'id': topic.id,
            'tittle': topic.tittle,
            'body': topic.body,
            'vote': len(topic.votes),
            'comment': len(topic.comments),
            'create_at': str(topic.create_at)
        })
    return jsonify(
        topics=res,
    ), HTTP_200_OK
