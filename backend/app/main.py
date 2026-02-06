from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base

from app.routers import leaderboard
from app.routers.leaderboard import router as leaderboard_router


from .config import CORS_ORIGINS, DEBUG


# Import all models so they register with Base.metadata
from .models import Team, Question, ChallengeSession, Submission

# Create database tables (must be after model imports)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BroCode Backend", version="1.0.0")
app.include_router(leaderboard_router)

# CORS middleware for frontend integration
import socket
import ipaddress

def get_network_ips():
    """Get all network IP addresses of this machine"""
    ips = []
    try:
        # Get all network interfaces
        hostname = socket.gethostname()
        for ip in socket.getaddrinfo(hostname, None):
            ip_addr = ip[4][0]
            if not ip_addr.startswith('127.') and ':' not in ip_addr:  # IPv4 only, not localhost
                ips.append(ip_addr)
    except:
        pass

    # Also try common methods
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        if local_ip not in ips and not local_ip.startswith('127.'):
            ips.append(local_ip)
        s.close()
    except:
        pass

    return list(set(ips))  # Remove duplicates

if DEBUG:
    # For LAN testing - allow localhost + detected network IPs
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Add detected network IPs
    network_ips = get_network_ips()
    for ip in network_ips:
        origins.extend([
            f"http://{ip}:5173",
            f"http://{ip}:3000",
        ])

    allow_credentials = True  # Now we can use credentials with specific origins
    print(f"CORS configured for LAN testing: allowing origins {origins}")
else:
    # Production configuration
    origins = [origin.strip() for origin in CORS_ORIGINS if origin.strip()]
    if not origins:
        origins = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
    allow_credentials = True
    print(f"CORS configured with origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
try:
    from .routers import auth, questions, challenge, admin, admin_auth, leaderboard
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
    app.include_router(challenge.router, prefix="/api/challenge", tags=["Challenge"])
    app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
    app.include_router(admin_auth.router, prefix="/api/admin/auth", tags=["Admin Auth"])
    app.include_router(leaderboard.router)
    print("Routers registered successfully")
except ImportError as e:
    print(f"Warning: Could not import routers: {e}")
    # Continue without routers for basic functionality

@app.get("/")
async def root():
    return {"message": "Welcome to BroCode Backend API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)