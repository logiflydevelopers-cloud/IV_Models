from app.models.model_registry import MODEL_REGISTRY


def remove_background(inputs: dict):

    model_handler = MODEL_REGISTRY["background_remove"].get(inputs["model"])

    if not model_handler:
        raise ValueError("Unsupported background remove model")

    image_url = inputs["image_url"]

    return model_handler(image_url)


def change_background(inputs: dict):

    model_handler = MODEL_REGISTRY["background_change"].get(inputs["model"])

    if not model_handler:
        raise ValueError("Unsupported background change model")

    image_url = inputs["image_url"]
    prompt = inputs.get("prompt")

    return model_handler(image_url, prompt)