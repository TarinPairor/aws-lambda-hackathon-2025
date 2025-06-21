# Automated Content Moderation System

A serverless content moderation system that automatically detects inappropriate content in images and videos using YOLO object detection.

## Features

- **Image Processing**: Real-time analysis of uploaded images
- **Video Processing**: Frame-by-frame analysis of video content
- **S3 Integration**: Automatic processing of S3 uploads
- **Quarantine System**: Automatic isolation of forbidden content
- **Email Alerts**: SES notifications for detected violations
- **API Service**: REST API for manual content analysis

## Project Structure

```
content-moderator/
├── config.py              # Configuration settings
├── content_moderator.py   # Main content moderation class
├── lambda_function.py     # AWS Lambda handler for S3 triggers
├── api_service.py         # FastAPI service for manual processing
├── test_local.py          # Local testing script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── runs/detect/train/    # Your trained YOLO model
    └── weights/
        └── best.pt       # Trained model weights
```

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file with your AWS credentials and settings:

```bash
# AWS Configuration
AWS_REGION=us-east-1
S3_INPUT_BUCKET=your-input-bucket-name
S3_QUARANTINE_BUCKET=your-quarantine-bucket-name
S3_OUTPUT_BUCKET=your-output-bucket-name

# SES Configuration
SES_SENDER_EMAIL=your-sender@domain.com
SES_RECIPIENT_EMAIL=your-recipient@domain.com

# AWS Credentials (if not using IAM roles)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### 2. AWS Resources Setup

#### S3 Buckets
Create the following S3 buckets:
- **Input Bucket**: Where users upload images/videos
- **Quarantine Bucket**: Where forbidden content is stored
- **Output Bucket**: Where processed content is stored

#### SES Configuration
1. Verify your sender email address in SES
2. If in sandbox mode, verify recipient email addresses
3. Request production access if needed

#### Lambda Function
1. Create a new Lambda function
2. Runtime: Python 3.9
3. Handler: `lambda_function.lambda_handler`
4. Memory: 1024MB (minimum)
5. Timeout: 30 seconds
6. Environment variables: Add all variables from `.env`

#### S3 Trigger
1. Go to your input S3 bucket
2. Add event notification
3. Event type: `s3:ObjectCreated:*`
4. Destination: Your Lambda function

### 3. Local Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Test the system locally:
```bash
python test_local.py
```

Run the API service:
```bash
uvicorn api_service:app --reload
```

## Usage

### 1. S3 Automatic Processing
- Upload images to your input S3 bucket
- Lambda function automatically processes them
- Forbidden content is moved to quarantine bucket
- Clean content gets a "verified" tag
- Email alerts are sent for violations

### 2. API Service
The API service provides endpoints for manual processing:

#### Analyze Image
```bash
curl -X POST "http://localhost:8000/analyze-image" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

#### Analyze Video
```bash
curl -X POST "http://localhost:8000/analyze-video" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_video.mp4"
```

### 3. Response Format

#### Image Analysis Response
```json
{
  "success": true,
  "filename": "test.jpg",
  "has_forbidden_content": false,
  "detections": [
    {
      "class": "normal",
      "class_id": 1,
      "confidence": 0.95,
      "bbox": [100, 100, 200, 200]
    }
  ],
  "total_detections": 1
}
```

#### Video Analysis Response
```json
{
  "success": true,
  "filename": "test.mp4",
  "video_duration": 30.5,
  "total_frames_processed": 30,
  "forbidden_frames": [],
  "has_forbidden_content": false
}
```

## Model Configuration

The system uses your trained YOLO model with the following classes:
- 0: knife
- 1: normal
- 2: violence
- 3: weapons

Forbidden classes are: [0, 2, 3] (knife, violence, weapons)

## Deployment

### Lambda Deployment
1. Package your code:
```bash
pip install --target ./package -r requirements.txt
cd package
zip -r ../lambda_deployment.zip .
cd ..
zip -g lambda_deployment.zip *.py
```

2. Upload to Lambda:
```bash
aws lambda update-function-code \
    --function-name your-function-name \
    --zip-file fileb://lambda_deployment.zip
```

### API Gateway (Optional)
1. Create API Gateway
2. Add Lambda integration
3. Configure CORS
4. Deploy API

## Monitoring and Logging

- CloudWatch logs for Lambda function
- S3 access logs for bucket monitoring
- SES delivery status for email notifications

## Security Considerations

1. **IAM Roles**: Use least privilege principle
2. **S3 Bucket Policies**: Restrict access appropriately
3. **SES Verification**: Verify all email addresses
4. **Model Security**: Keep your trained model secure

## Troubleshooting

### Common Issues

1. **Model Loading Error**: Ensure model path is correct
2. **S3 Permission Error**: Check IAM roles and bucket policies
3. **SES Error**: Verify email addresses and region
4. **Memory Issues**: Increase Lambda memory allocation

### Debug Mode
Enable debug logging by setting environment variable:
```bash
DEBUG=true
```

## Support

For issues and questions:
1. Check CloudWatch logs
2. Verify AWS credentials and permissions
3. Test locally first
4. Check model file integrity 