# BroCode Challenge Platform

A full-stack web application for conducting coding challenges with a custom "Bro Code" programming language. Teams compete in time-bound coding challenges with file upload support and real-time progress tracking.

## 🏗️ Architecture

This project consists of two main components:

- **Frontend**: React application with modern UI/UX
- **Backend**: FastAPI server with SQLAlchemy ORM

## 📁 Project Structure

```
BroUI/
├── @frontend/               # React frontend application
│   ├── public/
│   │   └── BroCode_Documentation.pdf
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Application pages/routes
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
│   │   │   ├── challenge.py
│   │   │   └── admin.py
│   │   └── schemas/         # Pydantic schemas
│   ├── venv/                # Python virtual environment
│   ├── server.py            # Simple server runner
│   ├── run.py               # Development server runner
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Backend environment variables
│   └── .env.example         # Backend environment template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- SQLite (for development) or PostgreSQL (for production)

### Frontend Setup

```bash
cd @frontend

# Copy environment template
cp .env.example .env

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
cd backend

# Copy environment template
cp .env.example .env

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

The backend will be available at `http://localhost:8000`

## 🔧 Configuration

### Frontend Environment Variables (.env)

```env
# Backend API Configuration
VITE_API_BASE_URL=http://localhost:8000/api

# Application Configuration
VITE_APP_NAME=BroCode Challenge
VITE_APP_VERSION=1.0.0
```

### Backend Environment Variables (.env)

```env
# Database Configuration
# For development (SQLite)
DATABASE_URL=sqlite:///./brocode.db

# For production (PostgreSQL)
# DATABASE_URL=postgresql://username:password@localhost:5432/brocode_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Challenge Configuration
CHALLENGE_DURATION_MINUTES=180
MAX_QUESTIONS=30

# File Upload Configuration
UPLOAD_DIR=uploads
ALLOWED_EXTENSIONS=.homie
```

## 📚 API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

### Key API Endpoints

#### Authentication
- `POST /api/auth/login` - Team login
- `GET /api/auth/me` - Get current team info

#### Questions
- `GET /api/questions/public/all` - Get all active questions
- `GET /api/questions/public/{id}` - Get specific question

#### Challenge
- `POST /api/challenge/start` - Start challenge session
- `GET /api/challenge/status` - Get current challenge status
- `PUT /api/challenge/submission/{question_id}` - Update submission
- `POST /api/challenge/upload/{question_id}` - Upload solution file
- `POST /api/challenge/submit` - Submit entire challenge

#### Admin (Requires Authentication)
- `GET /api/admin/teams` - Manage teams
- `GET /api/admin/sessions` - View challenge sessions
- `GET /api/questions/` - CRUD operations for questions

## 🗄️ Database Schema

### Core Models

#### Team
- Team authentication and profile information
- USN-based identification system

#### Question
- Challenge problems with descriptions and test cases
- Difficulty levels and point values

#### ChallengeSession
- Time-bound coding sessions per team
- Session state management

#### Submission
- Individual question submissions
- File upload support for .homie files
- Status tracking (saved, flagged, submitted)

## 🎯 Features

### For Participants
- **Team-based Authentication**: Login with team leader USN and password
- **Documentation Access**: Download BroCode language documentation
- **Timed Challenges**: 3-hour coding sessions with auto-submit
- **Question Management**: Navigate through 30 questions with status tracking
- **File Upload**: Submit .homie files for code solutions
- **Progress Tracking**: Visual indicators for saved/flagged/unattempted questions
- **Real-time Timer**: Countdown with localStorage persistence

### For Administrators
- **Team Management**: Register and manage participating teams
- **Question Bank**: Create and manage coding challenges
- **Session Monitoring**: Track active challenge sessions
- **Results Analysis**: View submission statistics and results
- **Challenge Control**: Enable/disable challenges globally

## 🛠️ Development

### Frontend Development

```bash
cd @frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Backend Development

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
python run.py

# Or run the simple server
python server.py
```

### Database Migrations

The application uses SQLAlchemy with automatic table creation. For production deployments, consider using Alembic for proper migration management.

## 🚀 Deployment

### Frontend Deployment
```bash
cd @frontend
npm run build
# Deploy the dist/ directory to your web server
```

### Backend Deployment
```bash
cd backend

# Install production dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary

# Set production environment variables
export DATABASE_URL="postgresql://user:pass@host:port/db"
export SECRET_KEY="your-production-secret-key"

# Run with production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support or questions:
- Check the API documentation at `/docs`
- Review the BroCode language documentation
- Create an issue in the repository

## 🎉 Acknowledgments

- Built with React, FastAPI, and Tailwind CSS
- Inspired by competitive programming platforms
- Custom "Bro Code" programming language for unique challenges