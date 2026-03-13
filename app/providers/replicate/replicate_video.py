from app.providers.replicate.replicate_client import replicate_client
import time
import tempfile

# =========================================================
# MODELS
# =========================================================

ANIME_VIDEO_MODEL = "minimax/video-01-live"

TEXT_TO_VIDEO_MODEL = "luma/ray-2-540p"

IMAGE_TO_VIDEO_MODEL = "minimax/hailuo-02-fast"

# =========================================================
# TEXT-TO-VIDEO
# =========================================================

def text_to_video_luma(prompt: str):

    if not prompt:
        raise ValueError("prompt is required")

    output = replicate_client.run(
        TEXT_TO_VIDEO_MODEL,
        input={
            "loop": False,
            "prompt": prompt,
            "duration": 5,
            "aspect_ratio": "9:16"
        }
    )

    # Handle FileOutput correctly
    if isinstance(output, list):
        first = output[0]
        return first.url if hasattr(first, "url") else first

    # Single FileOutput
    if hasattr(output, "url"):
        return output.url

    return output

# =========================================================
# IMAGE-TO-VIDEO
# =========================================================

def image_to_video_hailuo(image_bytes: bytes, prompt: str):

    if not image_bytes:
        raise ValueError("Image bytes required")
    
    start_time = time.time()

    # Save bytes → temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            output = replicate_client.run(
                IMAGE_TO_VIDEO_MODEL,
                input={
                    "prompt": prompt,
                    "go_fast": False,
                    "duration": 6,
                    "resolution": "512P",
                    "prompt_optimizer": True,
                    "first_frame_image": f
                }
            )

        # Normalize output → URL
        if isinstance(output, list) and len(output) > 0:
            item = output[0]
            video_url = item.url if hasattr(item, "url") else item
        elif hasattr(output, "url"):
            video_url = output.url
        else:
            raise RuntimeError(f"Unexpected output: {output}")

        return video_url

    except Exception as e:
        raise RuntimeError(f"Image → Video failed: {e}")
    
# =========================================================
# ANIME VIDEO GENERATION
# =========================================================

def anime_video(image_url: str, prompt: str):

    output = replicate_client.run(
        ANIME_VIDEO_MODEL,
        {
            "prompt": prompt,
            "prompt_optimizer": True,
            "first_frame_image": image_url
        }
    )

    # Normalize output → URL
    if isinstance(output, list) and len(output) > 0:
         item = output[0]
         video_url = item.url if hasattr(item, "url") else item
    elif hasattr(output, "url"):
         video_url = output.url
    else:
         raise RuntimeError(f"Unexpected output: {output}")

    return video_url
 