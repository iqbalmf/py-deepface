import uuid

from app.models.photo_model import Photo
from app.models.face_model import Face
from database import db
from sqlalchemy.orm import joinedload


def save_face(face_id, photo_id, bounding_box, descriptor):
    face = Face(
        id=face_id,
        photo_id=photo_id,
        bounding_box=bounding_box,
        descriptor=descriptor,
    )
    db.session.add(face)
    db.session.commit()
    return face

def get_faces_by_album_id(album_id):
    faces = (
        db.session.query(Face)
        .join(Photo)
        .filter(Photo.album_id == album_id)
        .options(joinedload(Face.photo))
        .all()
    )

    return [{
        "id": face.id,
        "photo_id": face.photo_id,
        "album_id": face.photo.album_id,
        "bounding_box": face.bounding_box,
        "descriptor": face.descriptor
    } for face in faces]
