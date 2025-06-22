from content_moderator import ContentModerator
import os
import requests
from PIL import Image
import io

def test_image_processing():
    """Test image processing functionality"""
    print("Testing image processing...")
    
    try:
        moderator = ContentModerator()
        print("Content moderator initialized successfully!")
        
        # Test with a sample image from the internet (or use local file)
        # test_image_url = "https://ultralytics.com/images/bus.jpg"  # Sample image with people and bus
        
        # print(f"Downloading test image from: {test_image_url}")
        # response = requests.get(test_image_url)
        # image_data = response.content
        test_image_path = r"/Users/tarinpairor/Downloads/knives.jpg"
        image_data = open(test_image_path, "rb").read()
        
        result = moderator.process_image(image_data)
        print(f"Image processing result: {result}")
        
        if result['success']:
            print(f"Detected {result['total_detections']} objects")
            for detection in result['detections']:
                print(f"  - {detection['class']} (confidence: {detection['confidence']:.2f})")
            
            if result['has_forbidden_content']:
                print("⚠️  FORBIDDEN CONTENT DETECTED!")
            else:
                print("✅ No forbidden content detected")
        
    except Exception as e:
        print(f"Error in image processing test: {e}")

def test_video_processing():
    """Test video processing functionality"""
    print("\nTesting video processing...")
    
    try:
        moderator = ContentModerator()
        
        # Test with a sample video (replace with your test video path)
        test_video_path = "test_video.mp4"  # Replace with actual test video path
        
        if os.path.exists(test_video_path):
            result = moderator.process_video(test_video_path)
            print(f"Video processing result: {result}")
            
            if result['success']:
                print(f"Processed {result['total_frames_processed']} frames")
                print(f"Video duration: {result['video_duration']:.2f} seconds")
                
                if result['forbidden_frames']:
                    print(f"⚠️  Found {len(result['forbidden_frames'])} frames with forbidden content")
                else:
                    print("✅ No forbidden content detected in video")
        else:
            print(f"Test video not found at {test_video_path}")
            print("Skipping video test...")
            
    except Exception as e:
        print(f"Error in video processing test: {e}")

def test_s3_simulation():
    """Test S3 handling simulation"""
    print("\nTesting S3 handling simulation...")
    
    try:
        moderator = ContentModerator()
        
        # Simulate S3 object processing
        test_bucket = "test-bucket"
        test_key = "test-image.jpg"
        
        print(f"Simulating S3 processing for: s3://{test_bucket}/{test_key}")
        print("Note: This is a simulation - no actual S3 operations will be performed")
        
        # For now, just test the image processing part
        test_image_url = "https://ultralytics.com/images/bus.jpg"
        response = requests.get(test_image_url)
        image_data = response.content
        
        result = moderator.process_image(image_data)
        
        if result['success']:
            if result['has_forbidden_content']:
                print("Simulation: Image would be moved to quarantine bucket")
                print("Simulation: Alert email would be sent")
            else:
                print("Simulation: Image would be tagged as verified")
        
    except Exception as e:
        print(f"Error in S3 simulation test: {e}")

if __name__ == "__main__":
    print("🚀 Starting Content Moderation System Tests")
    print("=" * 50)
    
    test_image_processing()
    test_video_processing()
    # test_s3_simulation()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!") 