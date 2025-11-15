#!/bin/bash
# Example script to train YOLOv8 on a trash dataset.
# You must prepare dataset in YOLO format: images/ and labels/ and a data.yaml file.

# pip install ultralytics
# Create data.yaml with paths to train/val and classes

ultralytics train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640 batch=16
# after training, copy best.pt to model path used by service
mv runs/detect/train/weights/best.pt ../backend/yolov8_trash_best.pt
