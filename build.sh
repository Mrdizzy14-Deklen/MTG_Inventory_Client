#!/bin/bash
./setup.sh
source venv/bin/activate
pyinstaller --onefile --name MTG_Inventory main.py
mkdir -p dist
if [ ! -f "dist/config.txt" ]; then
    echo "API_KEY=" > dist/config.txt
fi