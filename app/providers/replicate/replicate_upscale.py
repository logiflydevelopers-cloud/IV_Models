from app.providers.replicate.replicate_client import replicate_client

# =========================================================
# MODELS
# =========================================================

UPSCALE_MODEL = "recraft-ai/recraft-crisp-upscale"



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
# UPSCALE IMAGE
# =========================================================

async def upscale_image(inputs, settings=None):

    images = extract_images(inputs)

    if not images:
        raise ValueError("Image URL is required")

    # Replicate expects single image (string, not list)
    image_url = images[0]

    try:
        # FIX: pass dict directly (NO input=)
        output = replicate_client.run(
            UPSCALE_MODEL,
            {
                "image": image_url
            }
        )

        # Normalize response
        if isinstance(output, list) and len(output) > 0:
            item = output[0]
            return item.url if hasattr(item, "url") else item

        if hasattr(output, "url"):
            return output.url

        return output

    except Exception as e:
        raise RuntimeError(f"Upscale failed: {e}")