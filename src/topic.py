import uuid
from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from  flask_jwt_extended  import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from src.database import Users, db, Topics
import json


topics = Blueprint("topics",__name__,url_prefix="/api/v1/topics")

@topics.post('/create-topic')
@jwt_required()
def create_topics():
    tittle = request.json['tittle']
    body = request.json['body']
    user_id = get_jwt_identity()
    id = uuid.uuid4();
    
    # print(request.json)
    
    topic = Topics(id = id,tittle=tittle, body=body, user_id=user_id)
    db.session.add(topic)
    db.session.commit()

    return jsonify({
        'message': "topics created",
        'topics': {
            'tittle': tittle, "id": id
        }

    }), HTTP_201_CREATED

@topics.get('/my-topics')
@jwt_required()
def my_topics():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()
    res = []
    for topic in user.topic:
        res.append({
            'id':topic.id,
            'tittle':topic.tittle,
            'body':topic.body,
            'vote':len(topic.votes),
            'create_at':str(topic.create_at)
        })
    
    print(user.topic)
    return jsonify(
        topics=res,
    ), HTTP_200_OK