from app.models.model_registry import MODEL_REGISTRY


def generate_image(model: str, prompt: str):

    model_handler = MODEL_REGISTRY["image_generation"].get(model)

    if not model_handler:
        raise ValueError("Unsupported image generation model")

    return model_handler(prompt)


def upscale_image(model: str, image_url: str):

    model_handler = MODEL_REGISTRY["upscale"].get(model)

    if not model_handler:
        raise ValueError("Unsupported upscale model")

    return model_handler(image_url)