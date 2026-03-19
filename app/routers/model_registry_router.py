from fastapi import APIRouter

from app.models.model_registry import get_model_registry

router = APIRouter(
    prefix="/ai/models",
    tags=["Model Registry"]
)


# ==========================================================
# GET FULL REGISTRY (FOR DJANGO SYNC)
# ==========================================================
@router.get("/registry")
def fetch_model_registry():

    registry = get_model_registry()

    return {
        "status": "success",
        "data": registry
    }


# ==========================================================
# GET MODELS BY FEATURE
# ==========================================================
@router.get("/{feature}")
def get_models_by_feature(feature: str):

    registry = get_model_registry()

    if feature not in registry:
        return {
            "status": "error",
            "message": f"Feature '{feature}' not found"
        }

    return {
        "status": "success",
        "feature": feature,
        "models": registry[feature]
    }


# ==========================================================
# GET SINGLE MODEL DETAILS
# ==========================================================
@router.get("/{feature}/{model}")
def get_model_details(feature: str, model: str):

    registry = get_model_registry()

    if feature not in registry:
        return {
            "status": "error",
            "message": f"Feature '{feature}' not found"
        }

    if model not in registry[feature]:
        return {
            "status": "error",
            "message": f"Model '{model}' not found in '{feature}'"
        }

    return {
        "status": "success",
        "feature": feature,
        "model": model,
        "details": registry[feature][model]
    }