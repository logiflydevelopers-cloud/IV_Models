from app.models.model_registry import MODEL_REGISTRY


def edit_image(inputs: dict):

    model = inputs["model"]

    model_handler = MODEL_REGISTRY["background_change"].get(model)

    if not model_handler:
        raise ValueError("Unsupported edit model")

    image_url = inputs["image_url"]
    prompt = inputs.get("prompt")

    return model_handler(image_url, prompt)