import boto3
import os
from content_moderator import ContentModerator
from config import *

def test_s3_quarantine():
    """Test the S3 quarantine functionality"""
    
    print("🧪 Testing S3 Quarantine Functionality")
    print("=" * 50)
    
    # Initialize content moderator
    try:
        moderator = ContentModerator()
        print("✅ Content moderator initialized")
    except Exception as e:
        print(f"❌ Error initializing content moderator: {e}")
        return
    
    # Test with your knife image
    test_image_path = "/Users/tarinpairor/Downloads/knives.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        return
    
    print(f"📸 Processing image: {test_image_path}")
    
    # Read the image
    with open(test_image_path, 'rb') as f:
        image_data = f.read()
    
    # Process the image
    result = moderator.process_image(image_data)
    
    if result['success']:
        print(f"🔍 Detected {result['total_detections']} objects:")
        for detection in result['detections']:
            print(f"  - {detection['class']} (confidence: {detection['confidence']:.2f})")
        
        if result['has_forbidden_content']:
            print("⚠️  FORBIDDEN CONTENT DETECTED!")
            print("This image would be quarantined in production.")
            
            # Show what would happen in S3
            print("\n📦 S3 Quarantine Simulation:")
            print(f"  Input bucket: {S3_INPUT_BUCKET}")
            print(f"  Quarantine bucket: {S3_QUARANTINE_BUCKET}")
            print("  Action: Image would be moved to quarantine bucket")
            print("  Action: Email alert would be sent")
        else:
            print("✅ No forbidden content detected")
            print("This image would be tagged as verified.")
    else:
        print(f"❌ Error processing image: {result['error']}")

def test_actual_s3_upload():
    """Test actual S3 upload and processing (requires AWS setup)"""
    
    print("\n🚀 Testing Actual S3 Upload")
    print("=" * 50)
    
    # Check if AWS credentials are configured
    try:
        s3_client = boto3.client('s3')
        print("✅ AWS credentials configured")
    except Exception as e:
        print(f"❌ AWS credentials not configured: {e}")
        print("Please run: aws configure")
        return
    
    # Check if buckets exist
    try:
        s3_client.head_bucket(Bucket=S3_INPUT_BUCKET)
        print(f"✅ Input bucket exists: {S3_INPUT_BUCKET}")
    except:
        print(f"❌ Input bucket not found: {S3_INPUT_BUCKET}")
        print("Please create the bucket first")
        return
    
    try:
        s3_client.head_bucket(Bucket=S3_QUARANTINE_BUCKET)
        print(f"✅ Quarantine bucket exists: {S3_QUARANTINE_BUCKET}")
    except:
        print(f"❌ Quarantine bucket not found: {S3_QUARANTINE_BUCKET}")
        print("Please create the bucket first")
        return
    
    # Upload test image
    test_image_path = "/Users/tarinpairor/Downloads/knives.jpg"
    if os.path.exists(test_image_path):
        print(f"📤 Uploading {test_image_path} to S3...")
        
        try:
            s3_client.upload_file(
                test_image_path, 
                S3_INPUT_BUCKET, 
                "knives.jpg"
            )
            print("✅ Image uploaded successfully!")
            print("If Lambda is configured, it should process this image automatically.")
        except Exception as e:
            print(f"❌ Error uploading: {e}")
    else:
        print(f"❌ Test image not found: {test_image_path}")

if __name__ == "__main__":
    test_s3_quarantine()
    test_actual_s3_upload() 