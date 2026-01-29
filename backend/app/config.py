from decouple import config
import os

# Database configuration
#DATABASE_URL = config("DATABASE_URL", default="postgresql://user:password@localhost/brocode_db")
DATABASE_URL = "sqlite:///./brocode.db" 

# JWT configuration
SECRET_KEY = config("SECRET_KEY", default="your-secret-key-here")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30))

# Application configuration
DEBUG = config("DEBUG", default=True, cast=bool)
CORS_ORIGINS = config("CORS_ORIGINS", default="http://localhost:5173,http://localhost:3000").split(",")

# Challenge configuration
CHALLENGE_DURATION_MINUTES = int(config("CHALLENGE_DURATION_MINUTES", default=180))  # 3 hours
MAX_QUESTIONS = int(config("MAX_QUESTIONS", default=30))

# File upload configuration
UPLOAD_DIR = config("UPLOAD_DIR", default="uploads")
ALLOWED_EXTENSIONS = set(config("ALLOWED_EXTENSIONS", default=".homie").split(","))

# Execute API (sandbox runner) configuration
EXECUTE_API_BASE_URL = config("EXECUTE_API_BASE_URL", default="")
EXECUTE_API_TOKEN = config("EXECUTE_API_TOKEN", default="")
EXECUTE_API_TIMEOUT_SECONDS = float(config("EXECUTE_API_TIMEOUT_SECONDS", default=15))

# External Judge API configuration
JUDGE_API_URL = config("JUDGE_API_URL", default="http://localhost:9000/judge")
JUDGE_API_TIMEOUT_SECONDS = float(config("JUDGE_API_TIMEOUT_SECONDS", default=30))

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)