from fastapi import APIRouter
from app.schemas.character_schemas import CharacterRequest
from app.pipelines.character_pipeline_service import generate_character_pipeline

router = APIRouter(
    prefix="/pipeline",
    tags=["Character Pipeline"]
)


@router.post("/character")
async def generate_character(request: CharacterRequest):

    user_data = request.model_dump()

    result = await generate_character_pipeline(
        user_data=user_data,
        style=request.style
    )

    return result