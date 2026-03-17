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

    print("\n==================== 🚀 NEW REQUEST ====================")
    print("📥 FULL REQUEST:", request.dict())

    # ======================================================
    # GET MODEL
    # ======================================================
    try:
        model_fn = get_model(
            request.feature,
            request.model
        )
        print("✅ MODEL FOUND:", request.feature, request.model)

    except ValueError as e:
        print("❌ MODEL LOOKUP FAILED:", str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # ======================================================
    # PREPROCESS INPUTS (IMPORTANT FIX)
    # ======================================================
    inputs = request.inputs or {}

    print("📦 ORIGINAL INPUTS:", inputs)

    # 🔥 TEMP FIX for your schema mismatch
    # (convert image_1 → image if needed)
    if "image_1" in inputs and "image" not in inputs:
        inputs["image"] = inputs["image_1"]

    print("🛠️ FINAL INPUTS:", inputs)

    # ======================================================
    # RUN MODEL
    # ======================================================
    try:
        print("⚡ RUNNING MODEL...")

        result = await model_fn(inputs)

        print("✅ MODEL RESULT:", result)

    except Exception as e:
        print("❌ MODEL EXECUTION FAILED")
        traceback.print_exc()   # 🔥 FULL STACK TRACE

        raise HTTPException(
            status_code=500,
            detail=f"Model execution failed: {str(e)}"
        )

    # ======================================================
    # RESPONSE
    # ======================================================
    return {
        "status": "success",
        "feature": request.feature,
        "model": request.model,
        "result_url": result
    }