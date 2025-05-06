import os, uuid
from app.utils.face_utils import get_face_embedding, compare_embeddings
from config import Config


def match_faces_from_album(input_image, album_images):
    upload_dir = os.path.join(Config.UPLOAD_FOLDER, str(uuid.uuid4()))
    os.makedirs(upload_dir, exist_ok=True)

    input_path = os.path.join(upload_dir, "input.jpg")
    input_image.save(input_path)
    input_emb = get_face_embedding(input_path)

    matched_files = []
    for img in album_images:
        filename = f"{uuid.uuid4()}_{img.filename}"
        img_path = os.path.join(upload_dir, filename)
        img.save(img_path)

        emb = get_face_embedding(img_path)
        if compare_embeddings(input_emb, emb):
            matched_files.append(filename)

    return {"matched": len(matched_files) > 0, "matched_photos": matched_files}