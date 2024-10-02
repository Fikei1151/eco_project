from fer import FER

detector = FER(mtcnn=True)

def detect_emotion(face_image):
    result = detector.detect_emotions(face_image)
    if result:
        emotions = result[0]["emotions"]
        emotion = max(emotions, key=emotions.get)
        return emotion
    return None
