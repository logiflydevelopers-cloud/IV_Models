from app.providers.fal.fal_client import fal


# =========================================================
# MODELS
# =========================================================

BRIA_BG_REMOVE_MODEL = "fal-ai/bria/background/remove"

BG_DIFFUSION_MODEL = "fal-ai/image-editing/background-change"


# =========================================================
# BACKGROUND REMOVE
# =========================================================

def remove_background(image_url: str):
    """
    Remove background using BRIA model
    """

    arguments = {
        "image_url": image_url
    }

    try:
        result = fal.run(
            BRIA_BG_REMOVE_MODEL,
            arguments=arguments
        )

        if "images" in result:
            return result["images"][0]["url"]

        if "image" in result:
            return result["image"]["url"]

        raise RuntimeError(f"Unexpected response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai Bria diffusion failed: {e}")


# =========================================================
# BACKGROUND DIFFUSION / CHANGE
# =========================================================

def change_background(image_url: str, prompt: str):
    """
    Replace background using diffusion model
    """

    arguments = {
        "image_url": image_url,
        "prompt": prompt,
        "guidance_scale": 3.5,
        "num_inference_steps": 30,
        "safety_tolerance": "2",
        "output_format": "jpeg"
    }

    try:
        result = fal.run(
            BG_DIFFUSION_MODEL,
            arguments=arguments
        )

        if "images" in result:
            return result["images"][0]["url"]

        if "image" in result:
            return result["image"]["url"]

        raise RuntimeError(f"Unexpected response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai Bria diffusion failed: {e}")