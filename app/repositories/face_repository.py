from database import db
from app.models.face_model import Face


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
