from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BroCode Backend", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
try:
    from .routers import auth, questions, challenge, admin, admin_auth, leaderboard
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
    app.include_router(challenge.router, prefix="/api/challenge", tags=["Challenge"])
    app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
    app.include_router(admin_auth.router, prefix="/api/admin/auth", tags=["Admin Auth"])
    app.include_router(leaderboard.router, prefix="/api/leaderboard", tags=["Leaderboard"])
    print("Routers registered successfully")
except ImportError as e:
    print(f"Warning: Could not import routers: {e}")
    # Continue without routers for basic functionality

@app.get("/")
async def root():
    return {"message": "Welcome to BroCode Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)