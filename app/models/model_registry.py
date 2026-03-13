# FAL Providers
from app.providers.fal.fal_video import (
    text_to_video_kling,
    text_to_video_veo,
    image_to_video_wan,
    image_to_video_kling_element,
    generate_character_video
)

from app.providers.fal.fal_image import charcter_generation
from app.providers.fal.fal_edit import edit_character
from app.providers.fal.fal_bg import remove_background, change_background

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
        "kling_2_5": text_to_video_kling,
        "veo3": text_to_video_veo,
        "luma_ray": text_to_video_luma
    },

    # =========================================
    # IMAGE → VIDEO
    # =========================================
    "image_to_video": {
        "wan_2_2": image_to_video_wan,
        "kling_element": image_to_video_kling_element,
        "hailuo": image_to_video_hailuo,
        "anime_video": anime_video,
        "character_video": generate_character_video
    },

    # =========================================
    # IMAGE GENERATION
    # =========================================
    "image_generation": {
        "realistic_character": charcter_generation,
        "anime_character": anime_generation
    },

    # =========================================
    # IMAGE EDIT
    # =========================================
    "image_edit": {
        "character_edit": edit_character,
        "anime_edit": edit_anime,
        "background_change": change_background
    },

    # =========================================
    # BACKGROUND REMOVE
    # =========================================
    "background_remove": {
        "bria": remove_background
    },

    # =========================================
    # UPSCALE
    # =========================================
    "upscale": {
        "recraft": upscale_image
    }

}