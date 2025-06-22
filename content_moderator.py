import boto3
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import io
import tempfile
import os
from datetime import datetime
from config import *

class ContentModerator:
    def __init__(self):
        try:
            # Initialize YOLO model - will download automatically if not present
            print(f"Loading YOLO model from: {MODEL_PATH}")
            self.model = YOLO(MODEL_PATH)
            print("YOLO model loaded successfully!")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            raise
        
        self.s3_client = boto3.client('s3', region_name=AWS_REGION)
        # print(f"S3 client initialized with region: {AWS_REGION}")
        self.ses_client = boto3.client('ses', region_name=AWS_REGION)
        
    def process_image(self, image_data):
        """
        Process a single image and return detection results
        """
        try:
            # Convert image data to PIL Image
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
                
            # Run inference
            results = self.model(image)[0]
            
            detections = []
            has_forbidden_content = False
            
            for box in results.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                if confidence >= CONFIDENCE_THRESHOLD:
                    detection = {
                        'class': CLASS_NAMES.get(class_id, f'unknown_{class_id}'),
                        'class_id': class_id,
                        'confidence': confidence,
                        'bbox': box.xyxy[0].tolist()
                    }
                    detections.append(detection)
                    
                    if class_id in FORBIDDEN_CLASSES:
                        has_forbidden_content = True
            
            return {
                'success': True,
                'has_forbidden_content': has_forbidden_content,
                'detections': detections,
                'total_detections': len(detections)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_video(self, video_path: str):
        """
        Process a video file and return detection results for each frame
        """
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            frame_interval = int(fps / VIDEO_FRAME_RATE)
            frame_results = []
            forbidden_frames = []
            
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Process every nth frame based on frame_interval
                if frame_count % frame_interval == 0:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    
                    # Process frame
                    result = self.process_image(pil_image)
                    
                    if result['success']:
                        frame_result = {
                            'frame_number': frame_count,
                            'timestamp': frame_count / fps,
                            'detections': result['detections'],
                            'has_forbidden_content': result['has_forbidden_content']
                        }
                        frame_results.append(frame_result)
                        
                        if result['has_forbidden_content']:
                            forbidden_frames.append(frame_result)
                
                frame_count += 1
                
                # Stop if video is too long
                if frame_count / fps > MAX_VIDEO_DURATION:
                    break
            
            cap.release()
            
            return {
                'success': True,
                'total_frames_processed': len(frame_results),
                'forbidden_frames': forbidden_frames,
                'frame_results': frame_results,
                'video_duration': frame_count / fps
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_s3_image(self, bucket_name: str, object_key: str) -> dict:
        """
        Handle S3 image upload - download, process, and take action
        """
        try:
            # Download image from S3
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            image_data = response['Body'].read()
            
            # Process image
            result = self.process_image(image_data)
            
            if result['success']:
                if result['has_forbidden_content']:
                    # Move to quarantine bucket
                    self._move_to_quarantine(bucket_name, object_key)
                    # Send alert email
                    self._send_alert_email(object_key, result['detections'])
                    return {
                        'action': 'quarantined',
                        'detections': result['detections']
                    }
                else:
                    # Add verified tag
                    self._add_verified_tag(bucket_name, object_key)
                    return {
                        'action': 'verified',
                        'detections': result['detections']
                    }
            else:
                return {
                    'action': 'error',
                    'error': result['error']
                }
                
        except Exception as e:
            return {
                'action': 'error',
                'error': str(e)
            }
    
    def _move_to_quarantine(self, source_bucket: str, object_key: str):
        """Move object to quarantine bucket"""
        try:
            # Copy to quarantine bucket
            self.s3_client.copy_object(
                Bucket=S3_QUARANTINE_BUCKET,
                CopySource={'Bucket': source_bucket, 'Key': object_key},
                Key=f"quarantined/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{object_key}"
            )
            
            # Delete from source bucket
            self.s3_client.delete_object(Bucket=source_bucket, Key=object_key)
            
        except Exception as e:
            print(f"Error moving to quarantine: {e}")
    
    def _add_verified_tag(self, bucket_name, object_key):
        """Add verified tag to S3 object"""
        try:
            self.s3_client.put_object_tagging(
                Bucket=bucket_name,
                Key=object_key,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'ContentModeration',
                            'Value': 'Verified'
                        }
                    ]
                }
            )
        except Exception as e:
            print(f"Error adding verified tag: {e}")


    def _send_alert_email(self, object_key: str, detections: list):
        """Send alert email via SES"""
        return
        try:
            detection_summary = "\n".join([
                f"- {d['class']} (confidence: {d['confidence']:.2f})"
                for d in detections
            ])
            
            subject = f"Content Moderation Alert - Forbidden Content Detected"
            body = f"""
            Forbidden content detected in file: {object_key}
            
            Detections:
            {detection_summary}
            
            The file has been moved to quarantine bucket.
            Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            self.ses_client.send_email(
                Source=SES_SENDER_EMAIL,
                Destination={'ToAddresses': [SES_RECIPIENT_EMAIL]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            
        except Exception as e:
            print(f"Error sending alert email: {e}") 