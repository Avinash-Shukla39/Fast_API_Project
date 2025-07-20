from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.services.video_service import VideoService
from app.services.encryption import decrypt_data
import uuid

router = APIRouter()
video_service = VideoService()

@router.post("/upload")
async def upload_video(video: UploadFile):
    try:
        if not video.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be a video")
        
        video_id = await video_service.upload_video(video)
        return {
            "video_id": video_id,
            "message": "Video uploaded and encrypted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream/{video_id}")
async def stream_video(video_id: str):
    try:
        # Validate video_id format
        uuid.UUID(video_id)
        
        video_data = video_service.get_video_stream(video_id)
        if not video_data:
            raise HTTPException(status_code=404, detail="Video not found")
        
        decrypted_data = decrypt_data(video_data['data'])
        
        return StreamingResponse(
            iter([decrypted_data]),
            media_type=video_data['content_type'],
            headers={"Content-Disposition": f"inline; filename={video_id}"}
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid video ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))