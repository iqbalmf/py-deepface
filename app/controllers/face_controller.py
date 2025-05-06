from flask import request, jsonify
from app.services.face_services import match_faces_from_album
from app.repositories.photo_repository import save_photo
from app.repositories.face_repository import save_face
from app.utils.face_utils import extract_faces_and_descriptors
import os, uuid
from config import Config

def match_album_controller():
    input_image = request.files.get("input")
    album_images = request.files.getlist("album")

    if not input_image or not album_images:
        return jsonify({"error": "Input and album required"}), 400

    result = match_faces_from_album(input_image, album_images)
    return jsonify(result)

def upload_album_controller():
    album_id = request.form.get("album_id")
    photos = request.files.getlist("photos")

    if not album_id or not photos:
        return jsonify({"error": "album_id and photos required"}), 400

    saved_files = []
    upload_dir = os.path.join(Config.UPLOAD_FOLDER, "albums", album_id)
    os.makedirs(upload_dir, exist_ok=True)

    for photo in photos:
        photo_id = str(uuid.uuid4())
        filename = f"{photo_id}_{photo.filename}"
        file_path = os.path.join(upload_dir, filename)
        photo.save(file_path)

        file_size = os.path.getsize(file_path)

        save_photo(
            photo_id=photo_id,
            album_id=album_id,
            file_name=filename,
            file_path=file_path,
            file_size=file_size,
            storage_used=file_size,
            price=0
        )

        faces = extract_faces_and_descriptors(file_path)
        for face in faces:
            save_face(
                face_id=face["face_id"],
                photo_id=photo_id,
                bounding_box=face["bounding_box"],
                descriptor=face["descriptor"]
            )

        saved_files.append(filename)

    return jsonify({"uploaded": saved_files})