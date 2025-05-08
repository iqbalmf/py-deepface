import os
import uuid

import numpy as np

from app.repositories.face_repository import save_face, get_faces_by_album_id
from app.repositories.photo_repository import save_photo
from app.utils.face_utils import extract_faces_and_descriptors, cosine_similarity, \
    extract_faces_and_descriptors_matching
from config import Config


def match_faces_from_album(image_file, album_id, threshold=0.5):
    query_descriptor = extract_faces_and_descriptors_matching(image_file)
    if query_descriptor is None:
        raise ValueError("No face detected in input image.")

    # Ambil semua face descriptor dari album
    faces = get_faces_by_album_id(album_id)

    matches = []
    for face in faces:
        stored_descriptor = np.array(face['descriptor'])
        similarity = cosine_similarity(np.array(query_descriptor[0]['descriptor']), stored_descriptor)
        if similarity > (1 - threshold):  # Semakin tinggi, semakin mirip
            matches.append({
                "face_id": face['id'],
                "photo_id": face['photo_id'],
                "similarity": similarity,
                "bounding_box": face['bounding_box'],
            })

    # Urutkan berdasarkan similarity terbesar
    matches = sorted(matches, key=lambda x: x["similarity"], reverse=True)

    return matches


def input_faces_from_image(input_images, album_id):
    saved_files = []
    upload_dir = os.path.join(Config.UPLOAD_FOLDER, "albums", album_id)
    os.makedirs(upload_dir, exist_ok=True)

    for photo in input_images:
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
    return
