from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class TextToVideoRequest(BaseModel):
    model: str
    prompt: str


class ImageToVideoRequest(BaseModel):
    model: str
    prompt: str
    image_url: HttpUrl


class MultiImageToVideoRequest(BaseModel):
    model: str
    prompt: str
    image_urls: List[HttpUrl]


class VideoResponse(BaseModel):
    video_url: HttpUrl