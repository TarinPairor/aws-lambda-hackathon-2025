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

# Model Configuration
MODEL_PATH = 'runs/detect/train/weights/best.pt'  # Path to your trained model
CLASS_NAMES = {
    0: 'knife',
    1: 'normal', 
    2: 'violence',
    3: 'weapons'
}

# Detection thresholds
CONFIDENCE_THRESHOLD = 0.5
FORBIDDEN_CLASSES = [0, 2, 3]  # knife, violence, weapons

# Video processing
VIDEO_FRAME_RATE = 1  # Process 1 frame per second
MAX_VIDEO_DURATION = 300  # Maximum 5 minutes 