from content_moderator import ContentModerator
import os

def test_image_processing():
    """Test image processing functionality"""
    print("Testing image processing...")
    
    moderator = ContentModerator()
    
    # Test with a sample image (replace with your test image path)
    test_image_path = "test_image.jpg"  # Replace with actual test image path
    
    if os.path.exists(test_image_path):
        with open(test_image_path, 'rb') as f:
            image_data = f.read()
        
        result = moderator.process_image(image_data)
        print(f"Image processing result: {result}")
    else:
        print(f"Test image not found at {test_image_path}")

def test_video_processing():
    """Test video processing functionality"""
    print("\nTesting video processing...")
    
    moderator = ContentModerator()
    
    # Test with a sample video (replace with your test video path)
    test_video_path = "test_video.mp4"  # Replace with actual test video path
    
    if os.path.exists(test_video_path):
        result = moderator.process_video(test_video_path)
        print(f"Video processing result: {result}")
    else:
        print(f"Test video not found at {test_video_path}")

if __name__ == "__main__":
    test_image_processing()
    test_video_processing() 