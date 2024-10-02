FROM python:3.12-slim

# ตั้งค่าไดเรกทอรีการทำงาน
WORKDIR /app

# คัดลอกไฟล์จำเป็นไปยังคอนเทนเนอร์
COPY ./app /app/app
# COPY ./worker /app/worker
COPY ./controller /app/controller
COPY requirements.txt /app/requirements.txt
COPY ./app/scripts /app/scripts
RUN mkdir -p /app/app/static/uploads && chmod -R 755 /app/app/static/uploads



# ติดตั้ง dependencies ที่จำเป็น รวมถึง 'file' และ 'bash'
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    dos2unix \
    file \
    build-essential \
    cmake \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpq-dev \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# แปลงไฟล์สคริปต์ด้วย dos2unix
RUN dos2unix /app/scripts/pipek-dash /app/scripts/pipek-worker

# ตั้งค่าสิทธิ์ในการรันสคริปต์
RUN chmod +x /app/scripts/pipek-dash /app/scripts/pipek-worker

# สร้าง virtual environment
RUN python3 -m venv /venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# ติดตั้งแพ็กเกจ Python ใน virtual environment
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    psycopg2-binary gunicorn flask
# ติดตั้ง torch และ torchvision สำหรับ CPU (ถ้าจำเป็น)
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# ตั้งค่า PYTHONPATH
ENV PYTHONPATH=/app

# เปิดพอร์ตที่ต้องการ
EXPOSE 8080

# จุดเริ่มต้นจะถูกกำหนดใน docker-compose.yml สำหรับแต่ละบริการ
