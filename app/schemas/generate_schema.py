from pydantic import BaseModel
from typing import Dict, Any, Optional


class GenerationRequest(BaseModel):

    feature: str
    model: str
    inputs: Dict[str, Any]
    settings: Optional[Dict[str, Any]] = None