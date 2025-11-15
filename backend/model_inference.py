# model_inference.py
import numpy as np
import cv2
from PIL import Image
import io

# This is a simple fallback detector; replace with YOLO if you install torch + ultralytics
class DummyDetector:
    def __init__(self):
        self.name = "dummy"

    def detect(self, image_bytes):
        # return list of detections [{'label':str, 'conf':float, 'bbox':[x1,y1,x2,y2]}]
        try:
            arr = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
        except Exception:
            # fallback cv2 decode
            nparr = np.frombuffer(image_bytes, np.uint8)
            arr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if arr is None:
                return []
            arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        _, th = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        dets = []
        for cnt in contours[:6]:
            x,y,w,h = cv2.boundingRect(cnt)
            if w*h < 200: 
                continue
            dets.append({
                "label": "litter",
                "conf": 0.45,
                "bbox": [float(x), float(y), float(x+w), float(y+h)]
            })
        return dets

detector = DummyDetector()
