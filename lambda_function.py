import json
import boto3
from content_moderator import ContentModerator
from config import *

def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda function triggered by S3 PutObject events
    """
    try:
        # Initialize content moderator
        moderator = ContentModerator()
        
        # Process S3 event
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            
            # Check if it's an image file
            if _is_image_file(object_key):
                print(f"Processing image: {object_key}")
                
                # Process the image
                result = moderator.handle_s3_image(bucket_name, object_key)
                
                print(f"Processing result: {result}")
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Image processed successfully',
                        'result': result
                    })
                }
            else:
                print(f"Skipping non-image file: {object_key}")
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'File is not an image, skipping processing'
                    })
                }
                
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def _is_image_file(filename: str) -> bool:
    """Check if file is an image based on extension"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    return any(filename.lower().endswith(ext) for ext in image_extensions) 