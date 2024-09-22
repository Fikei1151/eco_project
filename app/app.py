from flask import Flask, request, jsonify
from celery import Celery
import os
from model.yolo_model import detect_emotion

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Endpoint to handle image submission
@app.route('/submit-image', methods=['POST'])
def submit_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file.save(os.path.join('/tmp', file.filename))
    task = detect_emotion_task.apply_async(args=[file.filename])
    return jsonify({"task_id": task.id}), 202

@celery.task
def detect_emotion_task(filename):
    result = detect_emotion(os.path.join('/tmp', filename))
    # You can save the result to PostgreSQL here
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
