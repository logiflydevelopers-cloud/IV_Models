from app.providers.fal.fal_client import fal

# =========================================================
# MODELS
# =========================================================

BW_COLORIZE_MODEL = "fal-ai/ddcolor"

COLOR_CORRECTION = "fal-ai/image-editing/color-correction"



def extract_images(inputs):
    # Case 1: image_urls array (NEW FORMAT)
    if "image_urls" in inputs and isinstance(inputs["image_urls"], list):
        return inputs["image_urls"]

    # Case 2: single image_url
    if "image_url" in inputs:
        return [inputs["image_url"]]

    # Case 3: fallback (old dynamic keys)
    return [
        value for key, value in inputs.items()
        if key.startswith("image_") and value
    ]

# =========================================================
# BLACK AND WHITE COLORIZE
# =========================================================

async   def bw_colorize(inputs, settings=None):

    image_url = inputs["image_url"]

    arguments = {
        "image_url": image_url
        }

    try:
        result = fal.run(
            BW_COLORIZE_MODEL,
            arguments=arguments
        )

        if "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]

        if "image" in result:
            return result["image"]["url"]

        raise RuntimeError(f"Unexpected response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai background change failed: {e}")


# =========================================================
# COLOR CORRECTION
# =========================================================

async   def color_correction(inputs, settings=None):

    image_url = inputs["image_url"]

    arguments = {
        "image_url": image_url,
        "guidance_scale": 3.5,
        "num_inference_steps": 30,
        "safety_tolerance": "2",
        "output_format": "jpeg"
        }

    try:
        result = fal.run(
            BW_COLORIZE_MODEL,
            arguments=arguments
        )

        if "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]

        if "image" in result:
            return result["image"]["url"]

        raise RuntimeError(f"Unexpected response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai background change failed: {e}")
