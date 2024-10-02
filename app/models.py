from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    face_encoding = db.Column(db.PickleType)

class EmotionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    emotion = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
