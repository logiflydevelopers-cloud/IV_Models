from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.schemas.generate_schema import GenerationRequest
import traceback

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
    # PREPROCESS INPUTS (FIXED ✅)
    # ======================================================
    inputs = request.inputs or {}

    print("📦 ORIGINAL INPUTS:", inputs)

    try:
        # =========================================
        # 🔥 COLLECT ALL IMAGES (max 5)
        # =========================================
        image_keys = [f"image_{i}" for i in range(1, 6)]
        images = [inputs[k] for k in image_keys if k in inputs]

        print("🖼️ COLLECTED IMAGES:", images)

        # =========================================
        # 🔥 FEATURE-BASED VALIDATION
        # =========================================
        image_required_features = [
            "image_to_video",
            "background_remove",
            "background_change",
            "image_upscale",
            "image_colorize"
        ]

        if request.feature in image_required_features:
            if not images:
                raise Exception("At least one image is required")

            if len(images) > 5:
                raise Exception("Maximum 5 images allowed")

            # normalization only for image-based models
            inputs["image_url"] = images[0]
            inputs["image"] = images[0]
            inputs["images"] = images

        else:
            print("ℹ️ No image required for this feature")

        print("🛠️ FINAL INPUTS:", inputs)

    except Exception as e:
        print("❌ INPUT PROCESSING FAILED:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    # ======================================================
    # RUN MODEL
    # ======================================================
    try:
        print("⚡ RUNNING MODEL...")

        result = await model_fn(inputs)

        print("✅ MODEL RESULT:", result)

    except Exception as e:
        print("❌ MODEL EXECUTION FAILED")
        traceback.print_exc()

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