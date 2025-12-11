@echo off
title Starting Sara...

:: STEP 1 — Go to project root (THIS IS IMPORTANT)
cd /d "C:\Users\deera\SaraAI"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting backend from correct root...
start "Sara Backend" cmd /k python -m uvicorn backend.server:app --reload --port 8000

echo Starting frontend...
cd frontend
start "Sara UI" cmd /k npm run dev

echo Launching Sara in browser...
start http://localhost:5173/

echo Done.
exit
