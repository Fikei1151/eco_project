# worker/tasks.py

import cv2
import numpy as np
from app.utils.detection import detect_faces
from app.utils.recognition import get_face_encodings
from app.utils.emotion import detect_emotion
from app.models import db, User, EmotionData
from app import create_app
import face_recognition

app = create_app()
app.app_context().push()

def process_image(image_path):
    # โหลดภาพ
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # ตรวจจับใบหน้า
    faces = detect_faces(image)
    for (x1, y1, x2, y2) in faces:
        face_image = rgb_image[y1:y2, x1:x2]
        # ได้รับ face encodings
        face_encodings = get_face_encodings(face_image)
        if face_encodings:
            face_encoding = face_encodings[0]
            # ตรวจสอบว่ามีผู้ใช้นี้ในฐานข้อมูลหรือไม่
            users = User.query.all()
            known_encodings = [np.array(user.face_encoding) for user in users]
            known_names = [user.name for user in users]
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = None
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                user = users[first_match_index]
            else:
                # ถ้าไม่มี ให้สร้างผู้ใช้ใหม่ (ในที่นี้ใช้ชื่อ 'Unknown')
                user = User(name='Unknown', face_encoding=face_encoding)
                db.session.add(user)
                db.session.commit()
            # ตรวจจับอารมณ์
            emotion = detect_emotion(face_image)
            if emotion:
                # บันทึกอารมณ์ลงฐานข้อมูล
                emotion_data = EmotionData(user_id=user.id, emotion=emotion)
                db.session.add(emotion_data)
                db.session.commit()
    print(f"Processed image: {image_path}")
