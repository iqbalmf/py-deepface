import uuid
from deepface import DeepFace

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

def get_face_embedding(img_path):
    return DeepFace.represent(img_path=img_path, model_name='Facenet')[0]["embedding"]

def compare_embeddings(emb1, emb2, threshold=0.6):
    from numpy.linalg import norm
    return norm([a - b for a, b in zip(emb1, emb2)]) < threshold