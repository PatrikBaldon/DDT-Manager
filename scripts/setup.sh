#!/bin/bash

# DDT Electron App Setup Script
# This script sets up the development environment for Electron

set -e

echo "🚀 Setting up DDT Electron Application..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    echo "Visit: https://python.org/"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs media staticfiles tmp/pdfs backup static/pdf templates/pdf

# Copy environment file
if [ ! -f .env ]; then
    echo "📋 Creating .env file..."
    cp env.example .env
    echo "✅ .env file created. Please edit it with your settings."
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Run migrations
echo "🗄️ Running database migrations..."
python3 manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python3 manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ddt.local', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Collect static files
echo "📦 Collecting static files..."
python3 manage.py collectstatic --noinput

# Test Electron configuration
echo "🧪 Testing Electron configuration..."
if [ -f "electron/test.js" ]; then
    node electron/test.js
fi

echo "✅ Setup complete!"
echo ""
echo "🎉 DDT Electron Application is ready!"
echo ""
echo "To start the application:"
echo "  ./scripts/start-electron.sh"
echo "  or"
echo "  npm run electron-dev"
echo ""
echo "To access the application:"
echo "  Electron app will open automatically"
echo "  Django server: http://localhost:8000"
echo ""
echo "Admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "To stop the application:"
echo "  Close the Electron window or press Ctrl+C"
