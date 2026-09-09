# National Digital Bank AI Assistant

A full-stack banking assistant demo built with FastAPI and React. It includes secure authentication, a banking dashboard, transaction tracking, and an AI-style FAQ/chat assistant for customer support tasks.

## Overview

This project simulates a digital banking experience for a demo user. It provides:

- Signup and login with JWT authentication
- User profile and account summary
- Recent transaction history
- Banking FAQ assistant with intelligent keyword matching
- Chat history persistence
- Responsive frontend UI with light/dark theme support

## Tech stack

- Backend: FastAPI, SQLAlchemy, SQLite, JWT
- Frontend: React + Vite
- Styling: Custom CSS
- Authentication: Password hashing with secure backend functions

## Project structure

- backend/app.py — API routes and startup logic
- backend/auth.py — JWT and password helpers
- backend/chatbot.py — FAQ answer logic
- backend/database.py — database setup
- backend/models.py — SQLAlchemy models
- frontend/src/main.jsx — React app entry point
- frontend/src/styles.css — styling and layout

## Local setup

### 1) Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app:app --env-file .env --reload --host 0.0.0.0 --port 8000
```

For local demo data, keep `SEED_DEMO=true` in `backend/.env`. Never use that setting in production.

Backend URL:

- http://localhost:8000
- API docs: http://localhost:8000/docs

### 2) Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Frontend URL:

- http://localhost:5173

## Demo account

- Email: demo@ndb.com
- Password: Demo@123

## GitHub repository setup

From a terminal in this project folder:

```bash
git init -b main
git add .
git commit -m "Initial project setup"
```

Then create a new repository on GitHub and push:

```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

## Deployment options

### Option 1: Render backend + Vercel frontend

1. Push the code to GitHub. The root `render.yaml` can create the backend service.
2. In Render, create a PostgreSQL database and copy its internal connection URL.
3. Set these backend environment variables:

```text
ENVIRONMENT=production
JWT_SECRET_KEY=<a-long-random-secret>
DATABASE_URL=<Render PostgreSQL connection URL>
CORS_ORIGINS=https://<your-vercel-domain>
SEED_DEMO=false
```

4. If configuring the service manually, use these build/start commands:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 10000
```

5. Configure a health check at `/health`.

For the Vercel frontend, import the `frontend` folder and set:

```text
VITE_API_URL=https://<your-render-backend-domain>
```

Then add that Vercel URL to the backend `CORS_ORIGINS` value and redeploy the backend.

### Option 3: Local deployment

This project is already running locally in this workspace:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## Notes

- This is a demo application for educational and prototype use, not a real banking system.
- Do not use it with real bank credentials, real money, or production payment systems.
- Local development uses SQLite; production should use PostgreSQL through `DATABASE_URL`.
- Run database migrations and add rate limiting, audit logging, password reset, and stronger financial controls before handling sensitive users or money.

## Features included

- JWT signup/login
- User account and security flow
- Transaction dashboard
- Banking FAQ assistant
- Persistent chat history
- Responsive UI and theme-toggle styling
