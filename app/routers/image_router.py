from fastapi import APIRouter
from app.schemas.image_schemas import (
    ImageGenerationRequest,
    UpscaleRequest
)
from app.services.image_service import (
    generate_image,
    upscale_image
)

router = APIRouter(prefix="/image", tags=["Image"])


@router.post("/generate")
def create_image(request: ImageGenerationRequest):

    image_url = generate_image(
        request.model,
        request.prompt
    )

    return {"image_url": image_url}


@router.post("/upscale")
def upscale(request: UpscaleRequest):

    image_url = upscale_image(
        request.model,
        request.image_url
    )

    return {"image_url": image_url}