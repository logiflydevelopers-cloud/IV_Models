from pydantic import BaseModel, HttpUrl


class ImageEditRequest(BaseModel):
    model: str
    prompt: str
    image_url: HttpUrl


class BackgroundRemoveRequest(BaseModel):
    model: str
    image_url: HttpUrl


class BackgroundChangeRequest(BaseModel):
    model: str
    prompt: str
    image_url: HttpUrl


class EditResponse(BaseModel):
    image_url: HttpUrl