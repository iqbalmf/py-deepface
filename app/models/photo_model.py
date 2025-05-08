from database import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.String, primary_key=True)
    album_id = db.Column(db.String)
    file_name = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    file_size = db.Column(db.Integer)
    storage_used = db.Column(db.Integer)
    price = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    faces = relationship("Face", back_populates="photo")
