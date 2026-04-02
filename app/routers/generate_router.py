from fastapi import APIRouter, HTTPException
from app.schemas.generate_schema import GenerationRequest

from app.models.model_registry import get_model
from fal_client.client import FalClientHTTPError

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
        raise HTTPException(status_code=400, detail=str(e))

    # ======================================================
    # PREPROCESS INPUTS (FIXED + SAFE ✅)
    # ======================================================
    inputs = request.inputs or {}
    print("📦 ORIGINAL INPUTS:", inputs)

    try:
        images = []

        # -----------------------------------------
        # 1. image_1 → image_5
        # -----------------------------------------
        for i in range(1, 6):
            key = f"image_{i}"
            if inputs.get(key):
                images.append(str(inputs[key]))

        # -----------------------------------------
        # 2. image_url (string OR list)
        # -----------------------------------------
        if inputs.get("image_url"):
            if isinstance(inputs["image_url"], list):
                images.extend([str(img) for img in inputs["image_url"] if img])
            else:
                images.append(str(inputs["image_url"]))

        # -----------------------------------------
        # 3. image_urls (list)
        # -----------------------------------------
        if isinstance(inputs.get("image_urls"), list):
            images.extend([str(img) for img in inputs["image_urls"] if img])

        # -----------------------------------------
        # 4. image (single fallback)
        # -----------------------------------------
        if inputs.get("image"):
            images.append(str(inputs["image"]))

        # -----------------------------------------
        # 5. images (list fallback)
        # -----------------------------------------
        if isinstance(inputs.get("images"), list):
            images.extend([str(img) for img in inputs["images"] if img])

        # -----------------------------------------
        # ✅ CLEAN + DEDUPLICATE (SAFE)
        # -----------------------------------------
        images = list(dict.fromkeys(img for img in images if img))

        print("🖼️ COLLECTED IMAGES:", images)

        # =========================================
        # FEATURE VALIDATION
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
            # ✅ NORMALIZE (STRICT STANDARD)
            # =========================================
            inputs["image_url"] = images[0]     # keep your standard
            inputs["image_urls"] = images       # for multi-image models
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

    except FalClientHTTPError as e:
        print("❌ FAL ERROR:", e)

        error_data = e.args[0] if e.args else str(e)

        raise HTTPException(
            status_code=422,
            detail={
                "success": False,
                "source": "fal.ai",
                "error": error_data
            }
        )

    except Exception as e:
        print("❌ UNKNOWN ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "source": "internal",
                "error": str(e)
            }
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