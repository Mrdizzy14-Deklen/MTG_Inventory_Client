#!/bin/bash
PYTHON_CMD=$(command -v python3 || command -v python)

echo "Using $PYTHON_CMD to create virtual environment..."
$PYTHON_CMD -m venv venv
source venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "requirements.txt not found."
fi