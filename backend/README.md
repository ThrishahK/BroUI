# BroCode Backend (FastAPI + SQLite)

This is the backend API for the **BroCode Challenge Platform**.

- **Framework**: FastAPI
- **DB (default)**: SQLite (file: `brocode.db`)
- **ORM**: SQLAlchemy
- **Auth**: JWT (Bearer token)

---

## Project Layout

```
backend/
├── app/
│   ├── main.py              # FastAPI app (routers + DB init)
│   ├── database.py          # SQLAlchemy engine/session
│   ├── config.py            # env config (DATABASE_URL, JWT, etc)
│   ├── models/              # SQLAlchemy models
│   ├── routers/             # API routes
│   └── schemas/             # Pydantic schemas
├── brocode.db               # SQLite database file (created at runtime)
├── uploads/                 # uploaded .homie files
├── .env                     # runtime env (DO NOT COMMIT)
├── .env.example             # env template
├── requirements.txt         # python deps
├── server.py                # server entrypoint (runs app.main:app)
├── run.py                   # dev entrypoint (reload)
├── setup_database.py        # DB diagnostic / verify script
├── switch_database.py       # switch DATABASE_URL presets
└── README.md                # (this file)
```

---

## Requirements

- Python 3.10+ (you are using a venv already)
- `pip`

---

## Environment Setup

### 1) Create / activate venv

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment

```bash
cp .env.example .env
```

**Default DB is SQLite**:

```env
DATABASE_URL=sqlite:///./brocode.db
```

---

## Run (SQLite)

### Option A (recommended): normal server

```bash
cd backend
source venv/bin/activate
python switch_database.py sqlite
python setup_database.py
python server.py
```

### Option B: dev reload

```bash
cd backend
source venv/bin/activate
python run.py
```

Backend will be available at:
- `http://localhost:8000`

---

## Database (SQLite)

### Where the questions/accounts are stored

- SQLite file: `backend/brocode.db`
- The API reads questions from DB using:
  - `GET /api/questions/public/all`

### Verify DB quickly

```bash
cd backend
source venv/bin/activate
python setup_database.py
```

Expected output shows:
- SQLite version
- tables found: `teams`, `questions`, `challenge_sessions`, `submissions`

---

## Switching DB (keep SQLite for now)

You **asked to use SQLite**, so keep it on:

```bash
python switch_database.py sqlite
```

If later you want to switch for competition, you can update `DATABASE_URL` in `.env`.

---

## Test Accounts

We created these teams in SQLite:

- **USN**: `TEST123` | **Password**: `testpass`
- **USN**: `NNM24AC008` | **Password**: `NNM24AC008`

> Note: Password hashing is currently using a **bcrypt-first** approach, with a **SHA256 fallback** for the test accounts.

---

## How to Add New Teams (Accounts)

### Option A: API (quick)

Endpoint:
- `POST /api/auth/register?team_leader_usn=...&password=...&team_name=...`

Example:

```bash
curl -s -X POST "http://localhost:8000/api/auth/register?team_leader_usn=NNM24AC009&password=NNM24AC009&team_name=Team9"
```

### Option B: Direct SQLite insert (advanced)

You can insert into `teams` directly using SQLAlchemy / scripts (not recommended for normal use).

---

## How to Add Questions

There is **no admin UI** yet; you add questions via API.

### 1) Login to get a token

```bash
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"team_leader_usn":"TEST123","password":"testpass"}' | jq -r .access_token)
```

### 2) Create a question (admin endpoint)

```bash
curl -s -X POST "http://localhost:8000/api/questions/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Question",
    "description": "Write a BroCode program to ...",
    "sample_input": "",
    "sample_output": "",
    "difficulty": "easy",
    "points": 10
  }'
```

### 3) Verify public questions list

```bash
curl -s "http://localhost:8000/api/questions/public/all" | jq
```

---

## Core API Endpoints

### Auth
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/register` (query params)

### Questions
- `GET /api/questions/public/all`
- `GET /api/questions/public/{question_id}`
- `GET /api/questions/` (admin)
- `POST /api/questions/` (admin)
- `PUT /api/questions/{question_id}` (admin)
- `DELETE /api/questions/{question_id}` (admin)

### Challenge
- `POST /api/challenge/start`
- `GET /api/challenge/status`
- `PUT /api/challenge/submission/{question_id}`
- `POST /api/challenge/execute/{question_id}`  ✅ (calls Execute API, returns 1/0)
- `POST /api/challenge/upload/{question_id}`
- `POST /api/challenge/submit`

---

## Submitting answers (qnid + answer)

Each question has an **ID** (`question_id`). When the user types an answer in the UI and clicks **Save/Flag**, the frontend sends the answer to the backend using:

- **Endpoint**: `PUT /api/challenge/submission/{question_id}`
- **Path param**: `question_id` (this is the qnid)
- **JSON body**:
  - `code_answer`: string (the answer/code the user typed)
  - `status`: one of `saved`, `flagged`, `not_attempted`

Example:

```bash
curl -s -X PUT "http://localhost:8000/api/challenge/submission/12" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code_answer":"print(\"hello\")","status":"saved"}'
```

## Execute (sandbox judge) + locking rule

To judge a question, the frontend calls:

- `POST /api/challenge/execute/{question_id}`
- Body: `{ "code_answer": "..." }`

Response:
- `result`: `1` (correct) or `0` (wrong)
- `attempts`: how many executes were done
- `is_correct`: boolean
- `is_locked`: boolean (**true after correct**)

Rule implemented:
- You can execute multiple times **until you get correct**.
- Once correct, that question becomes **locked** (no more executes).

---

## Leaderboard

- `GET /api/leaderboard/`

Returns a ranked list of teams with:
- `rank`
- `team_name`
- `team_leader_usn`
- `solved`
- `score`

## File Uploads (.homie)

Upload endpoint:
- `POST /api/challenge/upload/{question_id}`

Files are stored in:
- `backend/uploads/`

---

## Security Notes (important)

- **DO NOT COMMIT** `backend/.env`.
- Always set a strong `SECRET_KEY`.
- Keep `DEBUG=True` only in development.

---

## Troubleshooting

### 1) Backend starts but endpoints are 404
- Make sure you are running `backend/server.py` (it imports `app.main:app`)
- Confirm routes are registered in `app/main.py`

### 2) Login fails
- Ensure the team exists in SQLite
- Use `/api/auth/register` to create a team

### 3) DB issues
- Run:

```bash
python setup_database.py
```

---

## Next (optional)

If you want, we can add a small **Admin UI** (frontend page) to:
- create teams
- create/edit questions

