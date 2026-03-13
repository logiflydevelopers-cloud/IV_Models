from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.routers.video_router import router as video_router
from app.routers.image_router import router as image_router
from app.routers.edit_router import router as edit_router
from app.routers.character_router import router as character_router


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI Gateway for Catch AI and Candy AI"
)


# =========================================================
# CORS (Allow your backends to call this service)
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(video_router)
app.include_router(image_router)
app.include_router(edit_router)
app.include_router(character_router)


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }