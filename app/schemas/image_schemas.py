from pydantic import BaseModel, HttpUrl


class ImageGenerationRequest(BaseModel):
    model: str
    prompt: str


class UpscaleRequest(BaseModel):
    model: str
    image_url: HttpUrl


class ImageResponse(BaseModel):
    image_url: HttpUrl