import os
import sys
from rq import Worker, Queue, Connection
import redis
from worker.tasks import process_image  # ตรวจสอบว่านำเข้าถูกต้องตามโครงสร้างไดเรกทอรี

# รับเส้นทางของไดเรกทอรีโปรเจกต์และเพิ่มเข้าไปใน sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)  # เพิ่มบรรทัดนี้เพื่อให้สามารถเข้าถึงโมดูลอื่นๆ ได้ถูกต้อง

redis_url = 'redis://redis:6379/0'
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(['default'])
        worker.work()
