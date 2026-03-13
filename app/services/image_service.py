from app.models.model_registry import MODEL_REGISTRY


def generate_image(inputs: dict):

    model = inputs["model"]

    model_handler = MODEL_REGISTRY["image_generation"].get(model)

    if not model_handler:
        raise ValueError("Unsupported image generation model")

    prompt = inputs["prompt"]

    return model_handler(prompt)


def upscale_image(inputs: dict):

    model = inputs["model"]

    model_handler = MODEL_REGISTRY["image_upscale"].get(model)

    if not model_handler:
        raise ValueError("Unsupported upscale model")

    image_url = inputs["image_url"]

    return model_handler(image_url)