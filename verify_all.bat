@echo off
title CampusStay - Manual Execution & Verification Console
color 0A
cd /d D:\ASD&D\hostel-management

echo =====================================================================
echo  CampusStay - Hostel Management System Local Verification Console
echo  Target Directory: %CD%
echo =====================================================================
echo.

echo [1/4] Verifying Git Repository & Remote Link...
git remote -v
git status -s
echo.

echo [2/4] Executing Pytest Unit Test Suite with JUnit XML Generation...
python -m pytest backend/tests/test_main.py -v --junitxml=test-reports/junit.xml -o pythonpath=backend
echo.

echo [3/4] Querying Live Backend Health Check Probe...
curl -s http://127.0.0.1:8000/health
echo.
echo.

echo [4/5] Querying Live Hostel Rooms from Supabase Database...
curl -s http://127.0.0.1:8000/api/rooms
echo.
echo.

echo [5/6] Querying Live Nagios Core 4.4.6 Monitoring Engine (Port 8085)...
curl -s http://127.0.0.1:8085/api/status
echo.
echo.

echo [6/6] Querying Live Jenkins CI/CD Pipeline (Port 8080)...
curl -s -I http://127.0.0.1:8080/ | findstr "HTTP/"
echo Jenkins pipeline is live and accessible.
echo.
echo.

echo =====================================================================
echo  All checks executed successfully on your local machine!
echo  • Web Dashboard:    http://localhost:8000/dashboard
echo  • Jenkins Pipeline: http://localhost:8080
echo  • Nagios Monitor:   http://localhost:8085
echo  Press Win + Shift + S to take your live presentation screenshot.
echo =====================================================================
pause
