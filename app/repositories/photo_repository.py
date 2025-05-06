from app.models.photo_model import Photo
from database import db

def save_photo(photo_id, album_id, file_name, file_path, file_size, storage_used, price):
    photo = Photo(
        id=photo_id,
        album_id=album_id,
        file_name=file_name,
        file_path=file_path,
        file_size=file_size,
        storage_used=storage_used,
        price=price
    )
    db.session.add(photo)
    db.session.commit()
    return photo