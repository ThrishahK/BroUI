#!/usr/bin/env python3
import uvicorn
import os
import sys

# Add the current directory to Python path for proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    print(f"Starting server from: {os.getcwd()}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
