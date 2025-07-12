#!/bin/bash

# Local CI/CD simulation script
# This script simulates what GitHub Actions will do

echo "🚀 Starting local CI/CD simulation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check command success
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1 passed${NC}"
    else
        echo -e "${RED}❌ $1 failed${NC}"
        exit 1
    fi
}

echo -e "${YELLOW}📋 Step 1: Installing dependencies...${NC}"
pip install -r requirements.txt
pip install flake8 black isort mypy pytest-cov
check_status "Dependency installation"

echo -e "${YELLOW}🔍 Step 2: Running linting checks...${NC}"

echo "  • Running flake8..."
flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
check_status "Flake8 syntax check"

flake8 app --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
check_status "Flake8 style check"

echo "  • Checking code formatting with black..."
black --check app tests
check_status "Black formatting check"

echo "  • Checking import sorting with isort..."
isort --check-only app tests
check_status "Import sorting check"

echo "  • Running type checking with mypy..."
mypy app --ignore-missing-imports
check_status "Type checking"

echo -e "${YELLOW}🧪 Step 3: Running tests...${NC}"
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
check_status "Unit tests"

echo -e "${YELLOW}🔒 Step 4: Security scans...${NC}"
echo "  • Running bandit security scan..."
bandit -r app -f json -o bandit-report.json
echo "  • Security scan completed (check bandit-report.json)"

echo -e "${YELLOW}🐳 Step 5: Docker build test...${NC}"
docker build -t fastapi-feedback-app .
check_status "Docker build"

echo -e "${GREEN}🎉 All checks passed! Your code is ready for GitHub Actions.${NC}"
echo -e "${GREEN}✅ Linting passed${NC}"
echo -e "${GREEN}✅ Tests passed${NC}"
echo -e "${GREEN}✅ Security scans completed${NC}"
echo -e "${GREEN}✅ Docker image built successfully${NC}"
