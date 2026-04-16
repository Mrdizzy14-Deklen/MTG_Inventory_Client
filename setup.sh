#!/bin/bash

# Force python3.12
if command -v python3.12 &>/dev/null; then
    PYTHON_CMD=$(command -v python3.12)
else
    PYTHON_CMD=$(command -v python3 || command -v python)
fi

echo "Using $PYTHON_CMD to setup virtual environment..."

# Check for existing venv
if [ -d "venv" ]; then
    echo "Found existing venv. Upgrading/Refreshing..."
    $PYTHON_CMD -m venv --clear venv
else
    echo "Creating new venv..."
    $PYTHON_CMD -m venv venv
fi


source venv/bin/activate


echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
if [ -f requirements.txt ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Environment updated successfully."
else
    echo "requirements.txt not found. Environment is ready but empty."
fi