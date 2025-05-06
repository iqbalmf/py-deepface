from sqlalchemy.sql import func

from database import db


class Face(db.Model):
    __tablename__ = 'faces'
    id = db.Column(db.String, primary_key=True)
    photo_id = db.Column(db.String, db.ForeignKey('photos.id'), nullable=False)
    bounding_box = db.Column(db.JSON, nullable=False)
    descriptor = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())