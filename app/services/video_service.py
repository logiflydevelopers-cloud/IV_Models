from app.models.model_registry import MODEL_REGISTRY


def generate_text_to_video(model: str, prompt: str):

    model_handler = MODEL_REGISTRY["text_to_video"].get(model)

    if not model_handler:
        raise ValueError("Unsupported text-to-video model")

    return model_handler(prompt)


def generate_image_to_video(model: str, prompt: str, image_url):

    model_handler = MODEL_REGISTRY["image_to_video"].get(model)

    if not model_handler:
        raise ValueError("Unsupported image-to-video model")

    return model_handler(prompt, image_url)