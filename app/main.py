
from flask import Blueprint, render_template, request, redirect, url_for, flash
from redis import Redis
from rq import Queue
from werkzeug.utils import secure_filename
import os
import sys

# กำหนดประเภทไฟล์ที่อนุญาตให้อัพโหลด
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """ตรวจสอบว่าไฟล์ที่อัพโหลดมีนามสกุลที่อยู่ในรายการที่อนุญาตหรือไม่"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)  # เพิ่มเส้นทางโปรเจกต์เข้าไปใน sys.path

main = Blueprint('main', __name__)

redis_conn = Redis.from_url(os.environ.get('REDIS_URL'))  # ใช้ localhost ถ้าไม่มีการตั้งค่าเฉพาะ

q = Queue(connection=redis_conn)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)  # ใช้ secure_filename ป้องกันชื่อไฟล์ที่ไม่ปลอดภัย
            image_path = os.path.join('app', 'static', 'uploads', filename)
            image.save(image_path)
            q.enqueue('worker.tasks.process_image', image_path)
            return redirect(url_for('main.index'))
        else:
            flash('No image file or invalid file format.', 'error')  # แสดงข้อความเตือนเมื่อไม่มีไฟล์หรือรูปแบบไม่ถูกต้อง

    return render_template('index.html')
