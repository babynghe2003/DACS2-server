import uuid
from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from src.models import Users, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/create_admin')
def create_admin():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = Users(id=uuid.uuid4(), username=username,
            password=pwd_hash, email=email, role="admin")
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
            }

        }), HTTP_201_CREATED


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = Users(id=uuid.uuid4(), username=username,
            password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
            }

        }), HTTP_201_CREATED


@auth.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = Users.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                    }

                }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.patch('/update-profile')
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()

    for key in request.json:
        setattr(user, key, request.json[key])

    db.session.commit()
    return jsonify({
        'message': 'Update success',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username
            }
        }), HTTP_200_OK


@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
        }), HTTP_200_OK


@auth.get('/profile/<id>')
def profile(id):
    user = Users.query.filter_by(id=id).first()
    return jsonify(
            user
            ), HTTP_200_OK

@auth.put('/change-password')
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()

    old_password = request.json['old_password']
    new_password = request.json['new_password']

    if check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Password updated'}), HTTP_200_OK

    return jsonify({'error': 'Wrong password'}), HTTP_400_BAD_REQUEST
