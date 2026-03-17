from app.providers.fal.fal_client import fal

# =========================================================
# MODELS
# =========================================================

KLING_MODEL_ID = "fal-ai/kling-video/v2.5-turbo/pro/text-to-video"

VEO3_MODEL_ID = "fal-ai/veo3/fast"

WAN_MODEL_ID = "fal-ai/wan/v2.2-a14b/image-to-video/lora"

KLING_ELEMENT_MODEL_ID = "fal-ai/kling-video/v1.6/standard/elements"

CHARACTER_VIDEO_MODEL = "fal-ai/wan/v2.2-a14b/image-to-video/lora"

VEO_IMAGE_TO_VIDEO_MODEL_ID = "fal-ai/veo3.1/image-to-video"

# =========================================================
# TEXT-TO-VIDEO
# =========================================================

async   def text_to_video_kling(inputs):

    prompt = inputs["prompt"]

    arguments = {
        "prompt": prompt,
        "duration": 5,
        "aspect_ratio": "9:16",
        "negative_prompt": "blur, distort, and low quality",
        "cfg_scale": 0.5
    }

    try:
        result = fal.run(
            KLING_MODEL_ID,
            arguments=arguments
        )

        video = result.get("video")

        if not video:
            raise RuntimeError(f"No video returned from fal.ai: {result}")

        return video["url"]

    except Exception as e:
        raise RuntimeError(f"fal.ai Kling 2.5 failed: {e}")
    
# Veo 3 Model
VEO3_MODEL_ID = "fal-ai/veo3/fast"

async def text_to_video_veo(inputs):

    prompt = inputs["prompt"]

    arguments = {
        "prompt": prompt,
        "aspect_ratio": "9:16",
        "duration": "6s",
        "resolution": "720p",
        "generate_audio": True
    }

    try:
        result = fal.run(
            VEO3_MODEL_ID,
            arguments=arguments
        )

        video = result.get("video")

        if not video:
            raise RuntimeError(f"No video returned from fal.ai: {result}")

        return video["url"]

    except Exception as e:
        raise RuntimeError(f"fal.ai Veo failed: {e}")
    
# =========================================================
# IMAGE-TO-VIDEO
# =========================================================

def extract_images(inputs):
    return [
        value for key, value in inputs.items()
        if key.startswith("image_") and value
    ]

async def image_to_video_wan(inputs):
    try:
        prompt = inputs.get("prompt")
        if not prompt:
            raise ValueError("Prompt is required")

        images = extract_images(inputs)
        if not images:
            raise ValueError("At least one image is required")

        arguments = {
            "prompt": prompt,
            "negative_prompt": "bright colors, overexposed, static, blurred details, subtitles, style, artwork, painting, picture, still, overall gray, worst quality, low quality, JPEG compression residue, ugly, incomplete, extra fingers, poorly drawn hands, poorly drawn faces, deformed, disfigured, malformed limbs, fused fingers, still picture, cluttered background, three legs, many people in the background, walking backwards",
            "image_url": images[0],  # ✅ WAN supports single image
            "num_frames": 81,
            "frames_per_second": 16,
            "resolution": "720p",
            "num_inference_steps": 30,
            "guide_scale": 5,
            "shift": 5,
            "enable_safety_checker": False,
            "enable_prompt_expansion": False,
            "acceleration": "regular",
            "aspect_ratio": "9:16"
        }

        result = fal.run(WAN_MODEL_ID, arguments=arguments)

        if "video" in result:
            return result["video"]["url"]

        raise RuntimeError(f"Unexpected WAN response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai WAN failed: {e}")
    
async def image_to_video_kling_element(inputs):
    try:
        prompt = inputs.get("prompt")
        if not prompt:
            raise ValueError("Prompt is required")

        images = extract_images(inputs)
        if not images:
            raise ValueError("At least one image is required")

        arguments = {
            "prompt": prompt,
            "image_urls": images,  # ✅ MULTI IMAGE SUPPORT
            "duration": 5,
            "aspect_ratio": "9:16"
        }

        result = fal.run(KLING_ELEMENT_MODEL_ID, arguments=arguments)

        if "video" in result:
            return result["video"]["url"]

        raise RuntimeError(f"Unexpected Kling response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai Kling Element failed: {e}")
    

async def image_to_video_veo(inputs):
    try:
        prompt = inputs.get("prompt")
        if not prompt:
            raise ValueError("Prompt is required")

        images = extract_images(inputs)
        if not images:
            raise ValueError("At least one image is required")

        arguments = {
            "prompt": prompt,
            "aspect_ratio": "9:16",
            "duration": "6s",
            "resolution": "720p",
            "generate_audio": True,
            "image_url": images[0],  # ✅ single image
        }

        result = fal.run(VEO_IMAGE_TO_VIDEO_MODEL_ID, arguments=arguments)

        if "video" in result:
            return result["video"]["url"]

        raise RuntimeError(f"Unexpected VEO response: {result}")

    except Exception as e:
        raise RuntimeError(f"fal.ai VEO failed: {e}")
    
# =========================================================
# CHARACTER IMAGE-TO-VIDEO
# =========================================================

def generate_character_video(image_url: str, prompt: str):
    
    arguments = {
        "prompt": prompt,
        "negative_prompt": "bright colors, overexposed, static, blurred details, subtitles, style, artwork, painting, picture, still, overall gray, worst quality, low quality, JPEG compression residue, ugly, incomplete, extra fingers, poorly drawn hands, poorly drawn faces, deformed, disfigured, malformed limbs, fused fingers, still picture, cluttered background, three legs, many people in the background, walking backwards",
        "image_url": image_url,
        "num_frames": 81,
        "frames_per_second": 16,
        "resolution": "720p",
        "num_inference_steps": 30,
        "guide_scale": 5,
        "shift": 5,
        "enable_safety_checker": False,
        "enable_prompt_expansion": False,
        "acceleration": "regular",
        "aspect_ratio": "auto"
        }
    
    try:
        result = fal.run(
            CHARACTER_VIDEO_MODEL,
            arguments=arguments
        )

        video = result.get("video")
        if not video:
            raise RuntimeError(f"No image returned from fal.ai: {result}")

        return video["url"]

    except Exception as e:
        raise RuntimeError(f"wan-v2.2 failed: {e}")