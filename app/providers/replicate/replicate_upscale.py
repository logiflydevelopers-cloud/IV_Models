from app.providers.replicate.replicate_client import replicate_client

# =========================================================
# MODELS
# =========================================================

UPSCALE_MODEL = "recraft-ai/recraft-crisp-upscale"



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
# UPSCALE IMAGE
# =========================================================

def upscale_image(inputs, settings=None):

    image_url = extract_images(inputs)

    if not image_url:
        raise ValueError("Image URL is required")

    try:
        output = replicate_client.run(
            UPSCALE_MODEL,
            input={
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