@echo off
cd /d H:\Projects\subio2.0

REM якщо є venv — активуй його
REM call venv\Scripts\activate

waitress-serve --listen=127.0.0.1:8000 subio.wsgi:application

pause
