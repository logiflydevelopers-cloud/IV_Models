from pydantic import BaseModel
from typing import Dict, Any


class GenerationRequest(BaseModel):

    feature: str
    model: str
    inputs: Dict[str, Any]