import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_INPUT_BUCKET = os.getenv('S3_INPUT_BUCKET', 'YOUR_INPUT_BUCKET_NAME')
S3_QUARANTINE_BUCKET = os.getenv('S3_QUARANTINE_BUCKET', 'YOUR_QUARANTINE_BUCKET_NAME')
S3_OUTPUT_BUCKET = os.getenv('S3_OUTPUT_BUCKET', 'YOUR_OUTPUT_BUCKET_NAME')

# SES Configuration
SES_SENDER_EMAIL = os.getenv('SES_SENDER_EMAIL', 'YOUR_SENDER_EMAIL@domain.com')
SES_RECIPIENT_EMAIL = os.getenv('SES_RECIPIENT_EMAIL', 'YOUR_RECIPIENT_EMAIL@domain.com')

# Model Configuration - Using standard COCO model
MODEL_PATH = './yolov8n.pt'  # Standard YOLOv8 nano model with COCO classes
CLASS_NAMES = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus',
    6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant',
    11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
    16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
    22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag',
    27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard',
    32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
    36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle',
    40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
    46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli',
    51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair',
    57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet',
    62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
    67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink',
    72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors',
    77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
}

# Detection thresholds
CONFIDENCE_THRESHOLD = 0.5
# For testing: consider knife (43) and scissors (76) as "forbidden" items
FORBIDDEN_CLASSES = [43, 76]  # knife, scissors

# Video processing
VIDEO_FRAME_RATE = 1  # Process 1 frame per second
MAX_VIDEO_DURATION = 300  # Maximum 5 minutes 