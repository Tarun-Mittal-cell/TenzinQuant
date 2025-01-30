#!/bin/bash

# Exit on error
set -e

echo "Setting up QuantumTrader..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs
mkdir -p data

# Set up environment variables
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Created .env file from .env.example"
fi

echo "Setup complete! To start the application:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "2. Start the backend server:"
echo "   python server.py"
echo "3. In a new terminal, start the frontend:"
echo "   streamlit run main.py"