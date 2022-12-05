from flask import Flask, request
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.models import db
from src.topic import topics
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
            JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30)
        )

    else:
        app.config.from_mapping(test_config)

    @app.get("/")
    def index():
        
        return "Hello";

    @app.post("/api/v1/hello")
    def hello():
        data = request.json
        for i in data:
            print(i)
        return {"message": request.json['text']}
    db.app = app
    with app.app_context():
        db.init_app(app)
    
    CORS(app)
    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(topics)
    app.register_blueprint(dashboard)
    
    
    return app