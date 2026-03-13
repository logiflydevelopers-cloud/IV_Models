from fastapi import APIRouter
from app.schemas.edit_schemas import (
    ImageEditRequest,
    BackgroundRemoveRequest,
    BackgroundChangeRequest
)
from app.services.edit_service import edit_image
from app.services.bg_service import (
    remove_background,
    change_background
)

router = APIRouter(prefix="/edit", tags=["Edit"])


@router.post("/image")
def edit(request: ImageEditRequest):

    image_url = edit_image(
        request.model,
        request.image_url,
        request.prompt
    )

    return {"image_url": image_url}


@router.post("/remove-bg")
def remove_bg(request: BackgroundRemoveRequest):

    image_url = remove_background(
        request.model,
        request.image_url
    )

    return {"image_url": image_url}


@router.post("/change-bg")
def change_bg(request: BackgroundChangeRequest):

    image_url = change_background(
        request.model,
        request.image_url,
        request.prompt
    )

    return {"image_url": image_url}