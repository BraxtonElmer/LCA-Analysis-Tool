#!/bin/bash

# LCA Analysis Tool Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "🚀 Setting up AI-Driven LCA Analysis Tool..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3.11+ is installed
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo -e "${GREEN}✓ Python $python_version found${NC}"
else
    echo -e "${RED}✗ Python $required_version+ required, found $python_version${NC}"
    exit 1
fi

# Check if Node.js is installed
echo -e "${YELLOW}Checking Node.js version...${NC}"
if command -v node >/dev/null 2>&1; then
    node_version=$(node --version)
    echo -e "${GREEN}✓ Node.js $node_version found${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Setup environment file
echo -e "${YELLOW}Setting up environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Environment file created from template${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your configuration${NC}"
else
    echo -e "${GREEN}✓ Environment file already exists${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p logs media models staticfiles
echo -e "${GREEN}✓ Directories created${NC}"

# Run Django migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Database migrations completed${NC}"

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

# Setup frontend
echo -e "${YELLOW}Setting up frontend...${NC}"
cd frontend
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
cd ..

# Create superuser (optional)
echo -e "${YELLOW}Would you like to create a superuser? (y/N)${NC}"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# Load initial data
echo -e "${YELLOW}Loading initial data...${NC}"
python manage.py loaddata fixtures/materials.json 2>/dev/null || echo "No materials fixture found"
python manage.py loaddata fixtures/processes.json 2>/dev/null || echo "No processes fixture found"
python manage.py loaddata fixtures/circularity_indicators.json 2>/dev/null || echo "No circularity indicators fixture found"

echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo -e "${YELLOW}To start the development servers:${NC}"
echo -e "${GREEN}Backend:${NC} python manage.py runserver"
echo -e "${GREEN}Frontend:${NC} cd frontend && npm start"
echo -e "${GREEN}Celery Worker:${NC} celery -A lca_tool worker --loglevel=info"
echo -e "${GREEN}Celery Beat:${NC} celery -A lca_tool beat --loglevel=info"
echo ""
echo -e "${YELLOW}Access the application:${NC}"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}Backend API:${NC} http://localhost:8000/api"
echo -e "${GREEN}Admin Panel:${NC} http://localhost:8000/admin"
echo ""
echo -e "${YELLOW}Environment file:${NC} .env (update with your settings)"
echo -e "${YELLOW}Documentation:${NC} Check README.md for detailed usage instructions"
