# Protreptic Main FastAPI Application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.database import init_db
from api.routes import figures, modes, tags, search, export, health
from api.routes import thinking_modes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Protreptic API",
    description="Historical Figures Thinking Modes Library API",
    version="2.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(figures.router, prefix="/api/v1/scenarios", tags=["Figures"])
app.include_router(modes.router, prefix="/api/v1/modes", tags=["Modes"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["Tags"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(export.router, prefix="/api/v1", tags=["Export"])
app.include_router(thinking_modes.router, prefix="/api/v1", tags=["ThinkingModes"])


@app.get("/")
async def root():
    return {
        "name": "Protreptic API",
        "version": "2.1.0",
        "description": "Historical Figures Thinking Modes Library API",
        "docs": "/docs",
        "redoc": "/redoc",
    }