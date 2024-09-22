# model/yolo_model.py
import torch

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_emotion(image_path):
    results = model(image_path)
    # Processing results, for example, extracting expression detection data
    return results.pandas().xyxy[0].to_json(orient="records")
