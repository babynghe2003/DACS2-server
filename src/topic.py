import uuid
from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
        HTTP_409_CONFLICT, HTTP_405_METHOD_NOT_ALLOWED
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from src.models import Users, db, Topics, Comments, VoteTopic, VoteComment
from sqlalchemy import func, distinct
import json
from flask_mail import Mail, Message

topics = Blueprint("topics", __name__, url_prefix="/api/v1/topics")
mail = Mail()

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


# Like
@topics.post('/like-topic/<id>')
@jwt_required()
def like(id):
    user_id = get_jwt_identity()
    topic = Topics.query.filter_by(id=id).first()
    if topic:
        like = VoteTopic.query.filter_by(user_id=user_id, topic_id=id).first()
        if like:
            if like.vote_action == 1:
                db.session.delete(like)
                db.session.commit()
                return jsonify({
                    "message": "You unlike this topic"
                    }), HTTP_200_OK
            else:
                like.vote_action = 1
                db.session.commit()
                return jsonify({
                    "message": "You like this topic"
                    }), HTTP_200_OK
        else:
            like = VoteTopic(id=uuid.uuid4(), user_id=user_id, topic_id=id, vote_action=1)
            db.session.add(like)
            db.session.commit()
            return jsonify({
                "message": "You like this topic"
                }), HTTP_200_OK
    else:
        return jsonify({
            "message": "Video not found"
            }), HTTP_400_BAD_REQUEST

# Dislike
@topics.post('/dislike-topic/<id>')
@jwt_required()
def dislike(id):
    user_id = get_jwt_identity()
    topic = Topics.query.filter_by(id=id).first()
    if topic:
        like = VoteTopic.query.filter_by(user_id=user_id, topic_id=id).first()
        if like:
            if like.vote_action == 2:
                db.session.delete(like)
                db.session.commit()
                return jsonify({
                    "message": "You undislike this topic"
                    }), HTTP_200_OK
            else:
                like.vote_action = 2
                db.session.commit()
                return jsonify({
                    "message": "You dislike this topic"
                    }), HTTP_200_OK
        else:
            like = VoteTopic(id=uuid.uuid4(), user_id=user_id, topic_id=id, vote_action=2)
            db.session.add(like)
            db.session.commit()
            return jsonify({
                "message": "You dislike this topic"
                }), HTTP_200_OK
    else:
        return jsonify({
            "message": "Video not found"
            }), HTTP_404_NOT_FOUND


# Like comment
@topics.post('/like-comment/<id>')
@jwt_required()
def like_comment(id):
    user_id = get_jwt_identity()
    comment = Comments.query.filter_by(id=id).first()
    if comment:
        like = VoteComment.query.filter_by(user_id=user_id, comment_id=id).first()
        if like:
            if like.vote_action == 1:
                db.session.delete(like)
                db.session.commit()
                return jsonify({
                    "message": "You unlike this comment"
                    }), HTTP_200_OK
            else:
                like.vote_action = 1
                db.session.commit()
                return jsonify({
                    "message": "You like this comment"
                    }), HTTP_200_OK
        else:
            like = VoteComment(id=uuid.uuid4(), user_id=user_id, comment_id=id, vote_action=1)
            db.session.add(like)
            db.session.commit()
            return jsonify({
                "message": "You like this comment"
                }), HTTP_200_OK
    else:
        return jsonify({
            "message": "Comment not found"
            }), HTTP_400_BAD_REQUEST

# Dislike comment
@topics.post('/dislike-comment/<id>')
@jwt_required()
def dislike_comment(id):
    user_id = get_jwt_identity()
    comment = Comments.query.filter_by(id=id).first()
    if comment:
        like = VoteComment.query.filter_by(user_id=user_id, comment_id=id).first()
        if like:
            if like.vote_action == 2:
                db.session.delete(like)
                db.session.commit()
                return jsonify({
                    "message": "You undislike this comment"
                    }), HTTP_200_OK
            else:
                like.vote_action = 2
                db.session.commit()
                return jsonify({
                    "message": "You dislike this comment"
                    }), HTTP_200_OK
        else:
            like = VoteComment(id=uuid.uuid4(), user_id=user_id, comment_id=id, vote_action=2)
            db.session.add(like)
            db.session.commit()
            return jsonify({
                "message": "You dislike this comment"
                }), HTTP_200_OK
    else:
        return jsonify({
            "message": "Comment not found"
            }), HTTP_400_BAD_REQUEST


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
    like = VoteTopic.query.filter_by(user_id=get_jwt_identity(), topic_id=id).first()
    if like:
        like = like.vote_action
    else:
        like = 0
    for comment in topic.comments:
        like_comment = VoteComment.query.filter_by(user_id=get_jwt_identity(), comment_id=comment.id).first()
        if like_comment:
            like_comment = like_comment.vote_action
        else:
            like_comment = 0
        comments.append({
            "id": comment.id,
            "user_id": comment.user_id,
            "content": comment.content,
            "user": comment.user,
            "create_at": comment.create_at,
            "likes": len([i for i in comment.votes if i.vote_action == 1]) - len([i for i in comment.votes if i.vote_action == 2]),
            "is_like": like_comment
            })
    return jsonify({
        'topic': {
            "id": id,
            "title": topic.tittle,
            "body": topic.body,
            "user": topic.user,
            "create_at": topic.create_at,
            "likes": len([i for i in topic.votes if i.vote_action == 1]) - len([i for i in topic.votes if i.vote_action == 2]),
            "answers": len(topic.comments),
            "is_like": like
            },
        'comments': comments
        }
        ), HTTP_200_OK


@topics.delete('/delete-topic/<id>')
@jwt_required()
def delete_user(id):
    user_id = get_jwt_identity()
    topic = Topics.query.filter_by(id=id).first()
    user = Users.query.filter_by(id=user_id).first()
    print(id)
    if (topic.user_id != user_id and user.role != 'admin'):
        return jsonify({
            "message": "Not allowed"
            }), HTTP_405_METHOD_NOT_ALLOWED
    # Users.query.filter_by(id=id).delete()
    db.session.query(Topics).filter(Topics.id == id).delete()
    db.session.commit()
    return jsonify({
        'message': 'Delete success',
        }), HTTP_200_OK

@topics.get('/search')
def search():
    keyword = request.args.get('keyword')
    topicsList = Topics.query.filter(Topics.tittle.like(f'%{keyword}%')).all()
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

@topics.post('/report-topic/<id>')
@jwt_required()
def report_topic(id):
    user = Users.query.filter_by(id=get_jwt_identity()).first()
    topic = Topics.query.filter_by(id=id).first()
    msg = Message(subject="Report topic", sender="himinhpho44@gmail.com", recipients=["himinhpho@gmail.com"])
    msg.body = f"<strong>" + user.username + "</strong>" + " reported topic: " + f"<strong>" + topic.tittle + "</strong>"
    mail.send(msg)
    return jsonify({
        "message": "Report success"
        }), HTTP_200_OK

