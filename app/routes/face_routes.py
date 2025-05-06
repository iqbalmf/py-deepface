from flask import Blueprint
from app.controllers.face_controller import match_album_controller, upload_album_controller

face_bp = Blueprint('face', __name__)

face_bp.route('/match', methods=['POST'])(match_album_controller)
face_bp.route('/upload-album', methods=['POST'])(upload_album_controller)