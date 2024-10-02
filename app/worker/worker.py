# app/worker/worker.py

import os
import sys
from rq import Worker, Queue, Connection
import redis

# ไม่จำเป็นต้องปรับ sys.path อีกต่อไป

# นำเข้าโมดูลจากแพ็กเกจ app
from app import create_app
from app.models import db
from app.worker.tasks_module import process_image

redis_url = "redis://redis:6379/0"
conn = redis.from_url(redis_url)

if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(["default"])
        worker.work()
