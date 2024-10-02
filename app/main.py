# app/main.py

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from redis import Redis
from rq import Queue
from werkzeug.utils import secure_filename
import os
import sys
from app.models import db, User

# กำหนดประเภทไฟล์ที่อนุญาตให้อัพโหลด
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    """ตรวจสอบว่าไฟล์ที่อัพโหลดมีนามสกุลที่อยู่ในรายการที่อนุญาตหรือไม่"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)  # เพิ่มเส้นทางโปรเจกต์เข้าไปใน sys.path

main = Blueprint("main", __name__)

redis_url = os.environ.get(
    "REDIS_URL", "redis://redis:6379/0"
)  # กำหนดค่าเริ่มต้นหากไม่มี REDIS_URL
redis_conn = Redis.from_url(redis_url)

q = Queue(connection=redis_conn)


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files.get("image")
        if image and allowed_file(image.filename):
            filename = secure_filename(
                image.filename
            )  # ใช้ secure_filename ป้องกันชื่อไฟล์ที่ไม่ปลอดภัย

            # ใช้ current_app.root_path เพื่อให้ได้เส้นทางที่ถูกต้อง
            upload_folder = os.path.join(current_app.root_path, "static", "uploads")

            # ตรวจสอบและสร้างไดเรกทอรีหากไม่มีอยู่
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            image_path = os.path.join(upload_folder, filename)

            image.save(image_path)

            q.enqueue("app.worker.tasks_module.process_image", image_path)
            return redirect(url_for("main.index"))
        else:
            flash(
                "No image file or invalid file format.", "error"
            )  # แสดงข้อความเตือนเมื่อไม่มีไฟล์หรือรูปแบบไม่ถูกต้อง

    return render_template("index.html")


@main.route("/identify", methods=["GET", "POST"])
def identify():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        name = request.form.get("name")
        user = User.query.get(user_id)
        if user:
            user.name = name
            user.identified = True
            db.session.commit()
            flash("User identified successfully.", "success")
            return redirect(url_for("main.identify"))
    # ดึงผู้ใช้ที่ยังไม่ถูกระบุชื่อ
    unidentified_users = User.query.filter_by(identified=False).all()
    return render_template("identify.html", users=unidentified_users)
