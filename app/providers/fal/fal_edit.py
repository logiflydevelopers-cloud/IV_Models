from app.providers.fal.fal_client import fal

# =========================================================
# MODELS
# =========================================================

EDIT_MODEL = "fal-ai/qwen-image-2/pro/edit"

NANO_BANANA_2_EDIT = "fal-ai/nano-banana-2/edit"

# =========================================================
# CHARACTER EDIT
# =========================================================

def edit_character(image_url: list[str], prompt: str):
    """
    Edit Characters Using Qwen-Image-2 Edit model
    """
    
    arguments = {
        "prompt": prompt,
        "negative_prompt": "low resolution, error, worst quality, low quality, deformed",
        "enable_prompt_expansion": True,
        "enable_safety_checker": False,
        "num_images": 1,
        "output_format": "webp",
        "image_urls": [image_url],
        "image_size": {
            "width": 832,
            "height": 1232
        }
        }
    
    try:
        result = fal.run(
            EDIT_MODEL,
            arguments=arguments
        )

        image = result.get("images")
        if not image:
            raise RuntimeError(f"No image returned from fal.ai: {result}")

        return image[0]["url"]

    except Exception as e:
        raise RuntimeError(f"qwen-image-Edit failed: {e}")
    

async def image_edit(inputs):
    try:
        # ✅ Validate prompt
        prompt = inputs.get("prompt")
        if not prompt:
            raise ValueError("Prompt is required")

        # ✅ Collect all images dynamically (image_1, image_2, ...)
        images = [
            value for key, value in inputs.items()
            if key.startswith("image_") and value
        ]

        if not images:
            raise ValueError("At least one image is required")

        # ✅ Prepare payload for FAL
        arguments = {
            "prompt": prompt,
            "num_images": 1,
            "aspect_ratio": "9:16",
            "output_format": "png",
            "image_urls": images,  # ✅ MUST be list
            "resolution": "1K",
            "limit_generations": True
        }

        print("\n🟡 FAL REQUEST PAYLOAD:")
        print(arguments)

        # ✅ Run model
        result = fal.run(
            NANO_BANANA_2_EDIT,
            arguments=arguments
        )

        print("\n🟢 FAL RESPONSE:")
        print(result)

        # ✅ Handle response safely
        # (depends on model response format)
        if "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]

        if "image" in result:
            return result["image"]["url"]

        if "video" in result:
            return result["video"]["url"]

        # fallback debug
        raise RuntimeError(f"Unexpected FAL response format: {result}")

    except Exception as e:
        print("\n🔴 ERROR in image_edit:")
        print(str(e))
        raise RuntimeError(f"fal.ai nano-banana edit failed: {e}")