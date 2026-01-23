BroCode Challenge Platform
A full-stack web application for conducting coding challenges with a custom "Bro Code" programming language. Teams compete in time-bound coding challenges with file upload support and real-time progress tracking.

�️ Architecture
This project consists of three main components designed for offline reliability:

Frontend: React application with modern UI/UX.

Main Backend: FastAPI server with SQLAlchemy ORM for auth and data.

Execution API: A standalone service that runs student code against local test cases using the BroCode interpreter.

� Project Structure
Plaintext
BroUI/
├── @frontend/               # React frontend application
│   ├── public/
│   │   └── BroCode_Documentation.pdf
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Application pages/routes
│   │   │   └── Challenge.jsx # Main competition UI
│   │   ├── App.jsx          # Main application component
│   │   └── main.jsx         # Application entry point
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── .env                 # Frontend environment variables
│   └── .env.example         # Frontend environment template
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── main.py          # FastAPI application setup
│   │   ├── database.py      # Database configuration
│   │   ├── config.py        # Application configuration
│   │   ├── models/          # SQLAlchemy models
│   │   │   ├── team.py
│   │   │   ├── question.py
│   │   ├── routers/         # API route handlers
│   │   │   ├── auth.py
│   │   │   ├── questions.py
│   │   │   ├── challenge.py # Updated for local execution
│   │   │   └── admin.py
│   │   └── schemas/         # Pydantic schemas
│   ├── venv/                # Python virtual environment
│   ├── test_runner.py       # Local judging logic & subprocess runner [NEW]
│   ├── test_cases.json      # Question test cases (E01-H10) [NEW]
│   ├── runner_service.py    # Standalone Code Execution API [NEW]
│   ├── server.py            # Simple server runner
│   ├── run.py               # Development server runner
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Backend environment variables
│   └── .env.example         # Backend environment template
└── README.md
� Quick Start (Offline Procedure)
Prerequisites
Node.js (v16 or higher)

Python (v3.8 or higher)

SQLite (for development) or PostgreSQL (for production)

BroCode Interpreter: Install via pip install brocode-lang on the Master Laptop.

1. Standalone Execution API (Runner)
This service must be running for the "Execute" button to work.

Bash
cd backend
# Ensure virtual environment is active
python runner_service.py
The runner service will be available at http://localhost:8001.

2. Main Backend Setup
In a new terminal, start the primary application server.

Bash
cd backend
python server.py
The main API will be available at http://localhost:8000.

3. Frontend Setup
Bash
cd @frontend
npm install
npm run dev
� Configuration (Ethernet / Offline Event)
Networking
To run this in an offline environment over Ethernet:

Static IP: Set a static IP on the Master Laptop (e.g., 192.168.1.10).

Frontend .env: Point all participant laptops to the Master Laptop: VITE_API_BASE_URL=http://192.168.1.10:8000/api.

Host Binding: Run the servers with --host 0.0.0.0 to accept incoming Ethernet connections.

Backend Environment Variables (.env)
Code snippet
# Database Configuration
DATABASE_URL=sqlite:///./brocode.db

# Offline Execution Config
# Main backend will call this local address for code checking
EXECUTION_SERVICE_URL=http://localhost:8001/run
� API Documentation
Once the backend is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

�️ Database Schema
Core Models
Team
Team authentication and profile information

USN-based identification system

Question
Challenge problems with descriptions and test cases

Difficulty levels and point values

ChallengeSession
Time-bound coding sessions per team

Session state management

Submission
Individual question submissions

File upload support for .homie files

Status tracking (saved, flagged, submitted, passed)

� Features
For Participants
Team-based Authentication: Login with team leader USN and password

Documentation Access: Download BroCode language documentation

Offline Code Judging: Real-time evaluation using local test cases

Question Management: Navigate through 30 questions with status tracking

File Upload: Submit .homie files for code solutions

Automatic Locking: Once a question is marked PASS by the runner, it is locked in the UI

Real-time Timer: Countdown with localStorage persistence

For Administrators
Team Management: Register and manage participating teams

Question Bank: Create and manage coding challenges

Session Monitoring: Track active challenge sessions

Results Analysis: View submission statistics and results

Challenge Control: Enable/disable challenges globally

�️ Development
Frontend Development
Bash
cd @frontend
npm run dev          # Start development server
npm run build        # Build for production
Backend Development
Bash
cd backend
source venv/bin/activate
python run.py        # Run with auto-reload
� Deployment
Backend Deployment
Bash
# Set production environment variables
export DATABASE_URL="postgresql://user:pass@host:port/db"
uvicorn app.main:app --host 0.0.0.0 --port 8000
� License
This project is licensed under the MIT License - see the LICENSE file for details.

� Acknowledgments
Built with React, FastAPI, and Tailwind CSS

Custom "Bro Code" programming language for unique challenges