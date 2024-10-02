# app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    face_encoding = db.Column(db.PickleType)
    identified = db.Column(db.Boolean, default=False)  # เพิ่มฟิลด์นี้
    image_path = db.Column(db.String(255))  # เก็บเส้นทางของภาพผู้ใช้


class EmotionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    emotion = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
