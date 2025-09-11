@echo off
REM LCA Analysis Tool Setup Script for Windows
REM This script sets up the complete development environment on Windows

echo 🚀 Setting up AI-Driven LCA Analysis Tool...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo ✅ Node.js found

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
echo ✅ Python dependencies installed

REM Setup environment file
if not exist ".env" (
    echo Setting up environment configuration...
    copy .env.example .env
    echo ✅ Environment file created from template
    echo ⚠️  Please edit .env file with your configuration
) else (
    echo ✅ Environment file already exists
)

REM Create necessary directories
echo Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "media" mkdir media
if not exist "models" mkdir models
if not exist "staticfiles" mkdir staticfiles
echo ✅ Directories created

REM Run Django migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo ✅ Database migrations completed

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput
echo ✅ Static files collected

REM Setup frontend
echo Setting up frontend...
cd frontend
npm install
echo ✅ Frontend dependencies installed
cd ..

REM Create superuser (optional)
set /p create_superuser=Would you like to create a superuser? (y/N): 
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo To start the development servers:
echo Backend: python manage.py runserver
echo Frontend: cd frontend ^&^& npm start
echo Celery Worker: celery -A lca_tool worker --loglevel=info
echo Celery Beat: celery -A lca_tool beat --loglevel=info
echo.
echo Access the application:
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000/api
echo Admin Panel: http://localhost:8000/admin
echo.
echo Environment file: .env (update with your settings)
echo Documentation: Check README.md for detailed usage instructions

pause
