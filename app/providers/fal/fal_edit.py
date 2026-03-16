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

    prompt = inputs["prompt"]
    image_url = inputs["image_url"]

    arguments = {
        "prompt": prompt,
        "num_images": 1,
        "aspect_ratio": "9:16",
        "output_format": "png",
        "image_urls": image_url,
        "resolution": "1K",
        "limit_generations": True
        }

    try:
        result = fal.run(
            NANO_BANANA_2_EDIT,
            arguments=arguments
        )

        video = result.get("video")

        if not video:
            raise RuntimeError(f"No video returned from fal.ai: {result}")

        return video["url"]

    except Exception as e:
        raise RuntimeError(f"fal.ai Kling Element failed: {e}")