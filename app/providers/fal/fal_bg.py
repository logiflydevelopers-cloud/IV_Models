from app.providers.fal.fal_client import fal


# =========================================================
# MODELS
# =========================================================

BRIA_BG_REMOVE_MODEL = "fal-ai/bria/background/remove"

BG_DIFFUSION_MODEL = "fal-ai/image-editing/background-change"



def extract_images(inputs):
    images = [
        value for key, value in inputs.items()
        if key.startswith("image_") and value
    ]

    # ✅ fallback (old payload support)
    if not images and inputs.get("image_url"):
        images.append(inputs["image_url"])

    return images


# =========================================================
# BACKGROUND REMOVE
# =========================================================

async def remove_background(inputs):
    """
    Remove background using BRIA model
    """
    try:
        images = extract_images(inputs)

        if not images:
            raise ValueError("At least one image is required")

        image_url = images[0]  # ✅ only first image

        arguments = {
            "image_url": image_url
        }

        result = fal.run(
            BRIA_BG_REMOVE_MODEL,
            arguments=arguments
        )

        if "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]

        if "image" in result:
            return result["image"]["url"]

        raise RuntimeError(f"Unexpected response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai background removal failed: {e}")


# =========================================================
# BACKGROUND DIFFUSION / CHANGE
# =========================================================

async def change_background(inputs):
    """
    Replace background using diffusion model
    """
    try:
        prompt = inputs.get("prompt")
        if not prompt:
            raise ValueError("Prompt is required")

        images = extract_images(inputs)

        if not images:
            raise ValueError("At least one image is required")

        image_url = images[0]  # ✅ only first image

        arguments = {
            "image_url": image_url,
            "prompt": prompt,
            "guidance_scale": 3.5,
            "num_inference_steps": 30,
            "safety_tolerance": "2",
            "output_format": "jpeg"
        }

        result = fal.run(
            BG_DIFFUSION_MODEL,
            arguments=arguments
        )

        if "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]

        if "image" in result:
            return result["image"]["url"]

        raise RuntimeError(f"Unexpected response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai background change failed: {e}")