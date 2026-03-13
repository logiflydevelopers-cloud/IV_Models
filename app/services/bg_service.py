from app.models.model_registry import MODEL_REGISTRY


def remove_background(model: str, image_url: str):

    model_handler = MODEL_REGISTRY["background_remove"].get(model)

    if not model_handler:
        raise ValueError("Unsupported background remove model")

    return model_handler(image_url)


def change_background(model: str, image_url: str, prompt: str):

    model_handler = MODEL_REGISTRY["image_edit"].get(model)

    if not model_handler:
        raise ValueError("Unsupported background change model")

    return model_handler(image_url, prompt)