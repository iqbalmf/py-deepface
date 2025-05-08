import uuid

import numpy as np
from deepface import DeepFace
import cv2
import tempfile


def extract_faces_and_descriptors(file_path):
    try:
        representations = DeepFace.represent(img_path=file_path, model_name="Facenet", enforce_detection=False)
        results = []

        for rep in representations:
            descriptor = rep["embedding"]
            bounding_box = rep.get("facial_area", {})
            results.append({
                "face_id": str(uuid.uuid4()),
                "bounding_box": {
                    "x": bounding_box.get("x", 0),
                    "y": bounding_box.get("y", 0),
                    "w": bounding_box.get("w", 0),
                    "h": bounding_box.get("h", 0)
                },
                "descriptor": descriptor
            })
        return results
    except Exception as e:
        print("Error extracting face descriptor:", e)
        return []

def extract_faces_and_descriptors_matching(file):
    try:
        # Simpan ke file sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        # Jalankan DeepFace
        representations = DeepFace.represent(img_path=tmp_path, model_name="Facenet", enforce_detection=False)

        results = []
        for rep in representations:
            descriptor = rep["embedding"]
            bounding_box = rep.get("facial_area", {})
            results.append({
                "face_id": str(uuid.uuid4()),
                "bounding_box": {
                    "x": bounding_box.get("x", 0),
                    "y": bounding_box.get("y", 0),
                    "w": bounding_box.get("w", 0),
                    "h": bounding_box.get("h", 0)
                },
                "descriptor": descriptor
            })
        return results

    except Exception as e:
        print("Error extracting face descriptor:", e)
        return []


def extract_descriptor(image):
    img_np = read_image_as_numpy(image)
    result = DeepFace.represent(img_path=img_np, model_name='Facenet')[0]
    return np.array(result['embedding'])



def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def read_image_as_numpy(image_file):
    """
    Convert uploaded image (werkzeug FileStorage) to NumPy array.
    """
    # Simpan file sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image_file.save(tmp.name)
        tmp_path = tmp.name

    # Baca gambar dengan OpenCV dan ubah ke format RGB
    img_bgr = cv2.imread(tmp_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    return img_rgb
