import asyncio

from app.providers.openai.prompt_builder import (
    build_base_prompt,
    generate_pipeline_prompts
)

from app.services.image_service import generate_image
from app.services.edit_service import edit_image
from app.services.video_service import generate_image_to_video


# =========================================================
# CHARACTER PIPELINE
# =========================================================

async def generate_character_pipeline(user_data: dict, style: str):

    """
    Full character generation pipeline

    Outputs:
    - base image
    - 2 edited images
    - 2 videos
    """

    # -----------------------------------------------------
    # 1️⃣ BUILD BASE PROMPT
    # -----------------------------------------------------

    base_prompt = build_base_prompt(user_data)

    # -----------------------------------------------------
    # 2️⃣ GENERATE PIPELINE PROMPTS USING GPT
    # -----------------------------------------------------

    prompts = generate_pipeline_prompts(base_prompt)

    base_image_prompt = prompts["base_image_prompt"]
    edit_prompt_1 = prompts["edit_prompt_1"]
    edit_prompt_2 = prompts["edit_prompt_2"]
    video_prompt_1 = prompts["video_prompt_1"]
    video_prompt_2 = prompts["video_prompt_2"]

    # -----------------------------------------------------
    # 3️⃣ SELECT MODEL BASED ON CHARACTER TYPE
    # -----------------------------------------------------

    if  style == "anime":
        base_model = "anime_character"
        edit_model = "anime_edit"
        video_model = "anime_video"

    else:
        base_model = "realistic_character"
        edit_model = "character_edit"
        video_model = "character_video"

    # -----------------------------------------------------
    # 4️⃣ GENERATE BASE IMAGE
    # -----------------------------------------------------

    base_image = generate_image(base_model, base_image_prompt)

    # -----------------------------------------------------
    # 5️⃣ GENERATE EDITED IMAGES (PARALLEL)
    # -----------------------------------------------------

    edit_tasks = [
        asyncio.to_thread(
            edit_image,
            edit_model,
            base_image,
            edit_prompt_1
        ),
        asyncio.to_thread(
            edit_image,
            edit_model,
            base_image,
            edit_prompt_2
        )
    ]

    edited_images = await asyncio.gather(*edit_tasks)

    # -----------------------------------------------------
    # 6️⃣ GENERATE VIDEOS (PARALLEL)
    # -----------------------------------------------------

    video_tasks = [
        asyncio.to_thread(
            generate_image_to_video,
            video_model,
            edited_images[0],
            video_prompt_1
        ),
        asyncio.to_thread(
            generate_image_to_video,
            video_model,
            edited_images[1],
            video_prompt_2
        )
    ]

    videos = await asyncio.gather(*video_tasks)

    # -----------------------------------------------------
    # 7️⃣ RETURN FINAL OUTPUT
    # -----------------------------------------------------

    return {
        "base_image": base_image,
        "edited_images": edited_images,
        "videos": videos
    }