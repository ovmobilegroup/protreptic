# Protreptic Simple FastAPI Application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Protreptic API",
    description="Historical Figures Thinking Modes Library API",
    version="2.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "Protreptic API",
        "version": "2.1.0",
        "description": "Historical Figures Thinking Modes Library API",
        "docs": "/docs",
        "redoc": "/redoc",
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.1.0",
        "scenarios_count": 1147,
        "modes_count": 42,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)