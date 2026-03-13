from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.schemas.generate_schema import GenerationRequest

from app.models.model_registry import get_model

router = APIRouter(
    prefix="/ai",
    tags=["AI Generation"]
)



@router.post("/generate")
async def generate(request: GenerationRequest):

    try:

        # get model function from registry
        model_fn = get_model(
            request.feature,
            request.model
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    try:

        # run AI model
        result = await model_fn(request.inputs)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Model execution failed: {str(e)}"
        )

    return {
        "status": "success",
        "feature": request.feature,
        "model": request.model,
        "result": result
    }