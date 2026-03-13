from app.models.model_registry import MODEL_REGISTRY


def generate_text_to_video(inputs: dict):

    model = inputs["model"]

    model_handler = MODEL_REGISTRY["text_to_video"].get(model)

    if not model_handler:
        raise ValueError("Unsupported text-to-video model")

    prompt = inputs["prompt"]

    return model_handler(prompt)


def generate_image_to_video(inputs: dict):

    model = inputs["model"]

    model_handler = MODEL_REGISTRY["image_to_video"].get(model)

    if not model_handler:
        raise ValueError("Unsupported image-to-video model")

    prompt = inputs.get("prompt")
    image_url = inputs["image_url"]

    return model_handler(prompt, image_url)