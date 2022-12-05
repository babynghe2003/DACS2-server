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

dashboard = Blueprint("dashboard", __name__, url_prefix="/api/v1/dashboard")


@dashboard.get('/total-users/<option>')
@jwt_required()
def total_users(option):
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()
    if (user.role != 'admin'):
        return jsonify({
            "message": "Not allowed"
        }), HTTP_405_METHOD_NOT_ALLOWED
    if (option == 'month'):
        return jsonify({
            "total": 200,
            "data": [
                {
                    "x": "2018-2",
                    "y": 20
                },
                {
                    "x": "2018-3",
                    "y": 200
                },
                {
                    "x": "2018-4",
                    "y": 50
                },
                {
                    "x": "2018-5",
                    "y": 100
                },
                {
                    "x": "2018-6",
                    "y": 230
                },
                {
                    "x": "2018-7",
                    "y": 600
                },
            ]}), HTTP_200_OK

    elif (option == 'year'):
        return jsonify({
            "total": 200,
            "data": [
                {
                    "x": "2018",
                    "y": 20
                },
                {
                    "x": "2019",
                    "y": 200
                },
                {
                    "x": "2020",
                    "y": 50
                },
                {
                    "x": "2021",
                    "y": 100
                },
                {
                    "x": "2022",
                    "y": 300
                },
                {
                    "x": "2018-7",
                    "y": 800
                },
            ]}), HTTP_200_OK
    return jsonify({
        "total": 10,
        "data": [
            {
                "x": "2018-2",
                "y": 20
            },
            {
                "x": "2018-3",
                "y": 200
            },
            {
                "x": "2018-4",
                "y": 50
            },
            {
                "x": "2018-5",
                "y": 100
            },
            {
                "x": "2018-6",
                "y": 230
            },
            {
                "x": "2018-7",
                "y": 600
            },
        ]
    }), HTTP_200_OK


@dashboard.get("/all-users")
@jwt_required()
def all_user():
    userList = Users.query.filter_by(role='user').all()
    return jsonify({
        "data": userList
    }), HTTP_200_OK


@dashboard.patch('/update-user/<id>')
@jwt_required()
def update_user(id):
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()
    if (user.role != 'admin'):
        return jsonify({
            "message": "Not allowed"
        }), HTTP_405_METHOD_NOT_ALLOWED
    user = Users.query.filter_by(id=id).first()

    email = request.json['email']
    username = request.json['username']
    number = request.json['number']
    address = request.json['address']

    user.email = email
    user.username = username
    user.number = number
    user.address = address

    user.verified = True
    db.session.commit()
    return jsonify({
        'message': 'Update success',
        'user': {
            'id': user.id,
            'email': user.email
        }
    }), HTTP_200_OK


@dashboard.delete('/delete-user/<id>')
@jwt_required()
def delete_user(id):
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()
    if (user.role != 'admin'):
        return jsonify({
            "message": "Not allowed"
        }), HTTP_405_METHOD_NOT_ALLOWED
    # Users.query.filter_by(id=id).delete()
    print(id)
    db.session.query(Users).filter(Users.id == id).delete()
    db.session.commit()
    return jsonify({
        'message': 'Delete success',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
    }), HTTP_200_OK


@dashboard.delete('/delete-topic/<id>')
@jwt_required()
def delete_topic(id):
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()
    if (user.role != 'admin'):
        return jsonify({
            "message": "Not allowed"
        }), HTTP_405_METHOD_NOT_ALLOWED
    # Users.query.filter_by(id=id).delete()
    print(id)
    db.session.query(Topics).filter(Topics.id == id).delete()
    db.session.commit()
    return jsonify({
        'message': 'Delete success'
    }), HTTP_200_OK
