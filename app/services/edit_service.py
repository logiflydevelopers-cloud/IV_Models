from app.models.model_registry import MODEL_REGISTRY


def edit_image(model: str, image_url: str, prompt: str):

    model_handler = MODEL_REGISTRY["image_edit"].get(model)

    if not model_handler:
        raise ValueError("Unsupported edit model")

    return model_handler(image_url, prompt)