from flask import request, jsonify

from app.services.face_services import match_faces_from_album, input_faces_from_image


def match_album_controller():
    input_image = request.files.get("image")
    album_id = request.form.get("album_id")

    if not input_image or not album_id:
        return jsonify({"error": "Input and album required"}), 400

    result = match_faces_from_album(input_image, album_id)
    if result:
        return jsonify({"match": result}), 200
    else:
        return jsonify({"message": "No match found"}), 404


def upload_album_controller():
    album_id = request.form.get("album_id")
    photos = request.files.getlist("photos")

    if not album_id or not photos:
        return jsonify({"error": "album_id and photos required"}), 400
    try:
        input_faces_from_image(photos, album_id)
        return jsonify({"uploaded": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
