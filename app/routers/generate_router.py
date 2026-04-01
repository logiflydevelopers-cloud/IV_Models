from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.schemas.generate_schema import GenerationRequest
import traceback

from app.models.model_registry import get_model
from fal_client.client import FalClientHTTPError

router = APIRouter(
    prefix="/ai",
    tags=["AI Generation"]
)


from fastapi import APIRouter, HTTPException, BackgroundTasks
from uuid import uuid4


# 🔥 temporary store (later Redis/DB use karjo)
jobs = {}


# ======================================================
# GENERATE (NON-BLOCKING ✅)
# ======================================================
@router.post("/generate")
async def generate(request: GenerationRequest, background_tasks: BackgroundTasks):

    print("\n==================== 🚀 NEW REQUEST ====================")
    print("📥 FULL REQUEST:", request.dict())

    # ======================================================
    # GET MODEL
    # ======================================================
    try:
        model_fn = get_model(request.feature, request.model)
        print("✅ MODEL FOUND:", request.feature, request.model)

    except ValueError as e:
        print("❌ MODEL LOOKUP FAILED:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    # ======================================================
    # PREPROCESS INPUTS (SAME LOGIC ✅)
    # ======================================================
    inputs = request.inputs or {}

    try:
        images = []

        for i in range(1, 6):
            key = f"image_{i}"
            if inputs.get(key):
                images.append(inputs[key])

        if inputs.get("image_url"):
            images.append(inputs["image_url"])

        if inputs.get("image"):
            images.append(inputs["image"])

        if isinstance(inputs.get("images"), list):
            images.extend([img for img in inputs["images"] if img])

        images = list(dict.fromkeys(images))

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

            inputs["image_url"] = images[0]
            inputs["image"] = images[0]
            inputs["images"] = images

        settings = request.settings or {}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ======================================================
    # 🔥 CREATE JOB (IMPORTANT)
    # ======================================================
    job_id = str(uuid4())

    jobs[job_id] = {
        "status": "processing",
        "result_url": None,
        "error": None,
        "feature": request.feature,
        "model": request.model
    }

    # ======================================================
    # RUN IN BACKGROUND (🔥 FIX)
    # ======================================================
    background_tasks.add_task(
        run_generation_task,
        job_id,
        model_fn,
        inputs,
        settings
    )

    # 👉 immediate response (NO TIMEOUT)
    return {
        "job_id": job_id,
        "status": "processing"
    }


# ======================================================
# BACKGROUND TASK
# ======================================================
async def run_generation_task(job_id, model_fn, inputs, settings):

    try:
        print(f"⚡ Running job: {job_id}")

        result = await model_fn(inputs, settings)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result_url"] = result

        print(f"✅ Job completed: {job_id}")

    except FalClientHTTPError as e:
        error_data = e.args[0] if e.args else str(e)

        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = {
            "source": "fal.ai",
            "error": error_data
        }

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = {
            "source": "internal",
            "error": str(e)
        }


# ======================================================
# STATUS API
# ======================================================
@router.get("/status/{job_id}")
async def get_status(job_id: str):

    job = jobs.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job