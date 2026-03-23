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
        # 🔥 COLLECT ALL IMAGES (UNIVERSAL)
        # =========================================
        images = []

        # 1. image_1 → image_5
        for i in range(1, 6):
            key = f"image_{i}"
            if inputs.get(key):
                images.append(inputs[key])

        # 2. image_url (🔥 your current case)
        if inputs.get("image_url"):
            images.append(inputs["image_url"])

        # 3. image (single generic key)
        if inputs.get("image"):
            images.append(inputs["image"])

        # 4. images array (future-proof)
        if isinstance(inputs.get("images"), list):
            images.extend([img for img in inputs["images"] if img])

        # ✅ remove duplicates
        images = list(dict.fromkeys(images))

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

            # =========================================
            # 🔥 NORMALIZE (STANDARD FORMAT)
            # =========================================
            inputs["image_url"] = images[0]
            inputs["image"] = images[0]
            inputs["images"] = images

        else:
            print("ℹ️ No image required for this feature")

        print("🛠️ FINAL INPUTS:", inputs)

        settings = request.settings or {}

    except Exception as e:
        print("❌ INPUT PROCESSING FAILED:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    # ======================================================
    # RUN MODEL
    # ======================================================
    try:
        print("⚡ RUNNING MODEL...")

        result = await model_fn(inputs, settings)

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