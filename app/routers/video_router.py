from fastapi import APIRouter
from app.schemas.video_schemas import (
    TextToVideoRequest,
    ImageToVideoRequest
)
from app.services.video_service import (
    generate_text_to_video,
    generate_image_to_video
)

router = APIRouter(prefix="/video", tags=["Video"])


@router.post("/text-to-video")
def text_to_video(request: TextToVideoRequest):

    video_url = generate_text_to_video(
        request.model,
        request.prompt
    )

    return {"video_url": video_url}


@router.post("/image-to-video")
def image_to_video(request: ImageToVideoRequest):

    video_url = generate_image_to_video(
        request.model,
        request.prompt,
        request.image_url
    )

    return {"video_url": video_url}