from flask import Flask
from app.routes.face_routes import face_bp
from config import Config
from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(face_bp)
    with app.app_context():
        db.create_all()
    return app
