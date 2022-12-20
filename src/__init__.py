from flask import Flask, request
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.models import db
from src.topic import topics, mail
from src.dashboard import dashboard
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime, timedelta

def create_app(test_config=None):
    app = Flask(__name__,
            instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
                SECRET_KEY=os.environ.get("SECRET_KEY"),
                SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
                SQLALCHEMY_TRACK_MODIFICATIONS=False,
                JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
                JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
                JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
                MAIL_SERVER=os.environ.get('MAIL_SERVER'),
                MAIL_PORT=os.environ.get('MAIL_PORT'),
                MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS'),
                MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
                MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
                # MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL'),
                )

    else:
        app.config.from_mapping(test_config)

    CORS(app)
    JWTManager(app)
    mail.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(topics)
    app.register_blueprint(dashboard)

    @app.get("/api/v1/hello")
    def hello():
        return {"message": "hello world"}
    db.app = app
    with app.app_context():
        db.init_app(app)



    return app
