#!/bin/bash

# gpx-track-workbench-flet - Run Script
# This script creates/activates the virtual environment and runs the app in desktop mode

set -e  # Exit on any error

echo "Starting gpx-track-workbench-flet..."

# Check if .venv directory exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating .venv..."
    python3 -m venv .venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements if flet_requirements.txt exists
if [ -f "flet_requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r flet_requirements.txt
else
    echo "No flet_requirements.txt found. Installing flet and reportlab..."
    pip install flet reportlab
fi

# Ensure storage directories exist
echo "Creating storage directories..."
mkdir -p storage/data
mkdir -p storage/temp

# Run the application in desktop mode
echo "Starting application in desktop mode..."
echo "Close the application window to stop the script."

# Run with flet in desktop view mode
python run_flet.py --view=desktop

echo "Application closed."