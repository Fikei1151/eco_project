import face_recognition

def get_face_encodings(face_image):
    face_encodings = face_recognition.face_encodings(face_image)
    return face_encodings
