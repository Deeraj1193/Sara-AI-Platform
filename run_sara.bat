@echo off
title Starting Sara...

:: Move to the folder ABOVE SaraAI
cd /d "C:\Users\deera"

echo Activating virtual environment...
call SaraAI\venv\Scripts\activate.bat

echo Starting backend from correct root...
start "Sara Backend" cmd /k python -m uvicorn SaraAI.backend.server:app --reload --port 8000

echo Starting frontend...
cd SaraAI\frontend
start "Sara UI" cmd /k npm run dev

echo Launching Sara in browser...
start http://localhost:5173/

echo Done.
exit
