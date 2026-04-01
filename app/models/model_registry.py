# FAL Providers
from app.providers.fal.fal_video import (
    text_to_video_kling,
    text_to_video_veo,
    image_to_video_wan,
    image_to_video_kling_element,
    image_to_video_kling_video_o3,
    generate_character_video,
    text_to_video_kling_3
)

from app.providers.fal.fal_image import character_generation
from app.providers.fal.fal_edit import edit_character, image_edit
from app.providers.fal.fal_bg import remove_background, change_background
from app.providers.fal.fal_colorize import bw_colorize, color_correction

# Replicate Providers
from app.providers.replicate.replicate_video import (
    text_to_video_luma,
    anime_video,
    image_to_video_hailuo
)

from app.providers.replicate.replicate_image import anime_generation
from app.providers.replicate.replicate_edit import edit_anime
from app.providers.replicate.replicate_upscale import upscale_image


MODEL_REGISTRY = {

    # =========================================
    # TEXT → VIDEO
    # =========================================
    "text_to_video": {
        "kling_2_5": {
            "handler": text_to_video_kling,
            "provider": "fal",
            "credit_cost": 5
        },
        "veo3": {
            "handler": text_to_video_veo,
            "provider": "fal",
            "credit_cost": 6
        },
        "luma_ray": {
            "handler": text_to_video_luma,
            "provider": "replicate",
            "credit_cost": 4
        },
        "kling_3": {
            "handler": text_to_video_kling_3,
            "provider": "fal",
            "credit_cost": 7
        }
    },

    # =========================================
    # IMAGE → VIDEO
    # =========================================
    "image_to_video": {
        "wan_2_2": {
            "handler": image_to_video_wan,
            "provider": "fal",
            "credit_cost": 5
        },
        "kling_element": {
            "handler": image_to_video_kling_element,
            "provider": "fal",
            "credit_cost": 6
        },
        "hailuo": {
            "handler": image_to_video_hailuo,
            "provider": "replicate",
            "credit_cost": 4
        },
        "anime_video": {
            "handler": anime_video,
            "provider": "replicate",
            "credit_cost": 4
        },
        "kling_video_o3": {
            "handler": image_to_video_kling_video_o3,
            "provider": "fal",
            "credit_cost": 6
        },
        "character_video": {
            "handler": generate_character_video,
            "provider": "fal",
            "credit_cost": 7
        }
    },

    # =========================================
    # IMAGE GENERATION
    # =========================================
    "image_generation": {
        "realistic_character": {
            "handler": character_generation,
            "provider": "fal",
            "credit_cost": 3
        },
        "anime_character": {
            "handler": anime_generation,
            "provider": "replicate",
            "credit_cost": 3
        }
    },

    # =========================================
    # IMAGE EDIT
    # =========================================
    "image_edit": {
        "character_edit": {
            "handler": edit_character,
            "provider": "fal",
            "credit_cost": 2
        },
        "anime_edit": {
            "handler": edit_anime,
            "provider": "replicate",
            "credit_cost": 2
        },
        "nano_banana": {
            "handler": image_edit,
            "provider": "fal",
            "credit_cost": 2
        }
    },

    # =========================================
    # BACKGROUND REMOVE
    # =========================================
    "background_remove": {
        "bria": {
            "handler": remove_background,
            "provider": "fal",
            "credit_cost": 1
        }
    },

    # =========================================
    # BACKGROUND CHANGE
    # =========================================
    "background_change": {
        "fal_bg_change": {
            "handler": change_background,
            "provider": "fal",
            "credit_cost": 2
        }
    },

    # =========================================
    # IMAGE UPSCALE
    # =========================================
    "upscale": {
        "recraft": {
            "handler": upscale_image,
            "provider": "replicate",
            "credit_cost": 2
        }
    },

    # =========================================
    # IMAGE COLORIZE
    # =========================================
    "colorize": {
        "color_correction": {
            "handler": color_correction,
            "provider": "fal",
            "credit_cost": 2
        },
        "bw_colorize": {
            "handler": bw_colorize,
            "provider": "fal",
            "credit_cost": 2
        }
    }
}


def get_model(feature: str, model: str):

    if feature not in MODEL_REGISTRY:
        raise ValueError(f"Invalid feature: {feature}")

    feature_models = MODEL_REGISTRY[feature]

    if model not in feature_models:
        raise ValueError(
            f"Invalid model '{model}' for feature '{feature}'"
        )

    return feature_models[model]["handler"]


def get_model_registry():

    clean_registry = {}

    for feature, models in MODEL_REGISTRY.items():
        clean_registry[feature] = {}

        for model_name, data in models.items():
            clean_registry[feature][model_name] = {
                "provider": data.get("provider"),
                "credit_cost": data.get("credit_cost")
            }

    return clean_registry