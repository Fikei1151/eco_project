import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://coe:CoEpasswd@postgresql:5432/aies_dashdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
