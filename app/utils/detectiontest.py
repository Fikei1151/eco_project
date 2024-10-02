import torch

# โหลดโมเดล YOLO ที่เทรนไว้
model = torch.hub.load('ultralytics/yolov5', 'custom', path='app/models/yolo_model.pt', force_reload=True)

def detect_faces(image):
    results = model(image)
    faces = results.xyxy[0]  # เอาผลลัพธ์การตรวจจับใบหน้า
    return faces
