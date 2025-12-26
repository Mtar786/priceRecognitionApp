#!/bin/bash

echo "Starting PriceFinder Backend Server..."
echo ""

cd backend

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment not found. Installing dependencies globally..."
fi

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py


