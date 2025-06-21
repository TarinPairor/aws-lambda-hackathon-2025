from ultralytics import YOLO
# import torch

print("Initializing YOLOv8 model...")
try:
    # Download and initialize the official YOLOv8 nano model
    model = YOLO('yolov8n.pt')  # This will download the official model
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

model.train(data='./content-moderation.yaml', epochs=100)

model.export(format='onnx', imgsz=640, batch=1)