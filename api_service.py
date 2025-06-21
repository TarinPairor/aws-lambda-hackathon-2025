from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import tempfile
import os
from content_moderator import ContentModerator

app = FastAPI(title="Content Moderation API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize content moderator
moderator = ContentModerator()

@app.get("/")
async def root():
    return {"message": "Content Moderation API - Upload images or videos for analysis"}

@app.post("/analyze-image")
async def analyze_image(file: UploadFile):
    """
    Analyze a single image for forbidden content
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        contents = await file.read()
        
        # Process image
        result = moderator.process_image(contents)
        
        if result['success']:
            return {
                "success": True,
                "filename": file.filename,
                "has_forbidden_content": result['has_forbidden_content'],
                "detections": result['detections'],
                "total_detections": result['total_detections']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-video")
async def analyze_video(file: UploadFile):
    """
    Analyze a video file for forbidden content
    """
    try:
        # Validate file type
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be a video")
        
        # Save video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_file_path = tmp_file.name
        
        try:
            # Process video
            result = moderator.process_video(tmp_file_path)
            
            if result['success']:
                return {
                    "success": True,
                    "filename": file.filename,
                    "video_duration": result['video_duration'],
                    "total_frames_processed": result['total_frames_processed'],
                    "forbidden_frames": result['forbidden_frames'],
                    "has_forbidden_content": len(result['forbidden_frames']) > 0
                }
            else:
                raise HTTPException(status_code=500, detail=result['error'])
                
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Handler for AWS Lambda
handler = Mangum(app) 