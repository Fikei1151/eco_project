# app/utils/detection.py

import cv2
import os

# โหลด Haar Cascade สำหรับการตรวจจับใบหน้า
cascade_path = cv2.data.haarcascades
face_cascade = cv2.CascadeClassifier(os.path.join(cascade_path, 'haarcascade_frontalface_default.xml'))

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ตรวจจับใบหน้า
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # แปลงผลลัพธ์ให้อยู่ในรูปแบบเดียวกับที่ใช้ในโค้ดเดิม
    results = []
    for (x, y, w, h) in faces:
        x1, y1, x2, y2 = x, y, x + w, y + h
        results.append((x1, y1, x2, y2))
    return results
