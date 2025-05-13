"""
Main entry point for the Veritaminal FastAPI backend
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, game, gameplay
from .models import SessionData

app = FastAPI(
    title="Veritaminal API",
    description="Backend API for the Veritaminal game",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(game.router, prefix="/api/game", tags=["Game Management"])
app.include_router(gameplay.router, prefix="/api/gameplay", tags=["Gameplay"])

@app.get("/")
async def root():
    """Root endpoint that provides API information"""
    return {
        "name": "Veritaminal API",
        "version": "1.0.0",
        "description": "Backend API for Veritaminal game",
        "documentation": "/docs"
    }