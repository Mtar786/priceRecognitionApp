@echo off
echo Starting PriceFinder Backend Server...
echo.
cd backend
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Virtual environment not found. Installing dependencies globally...
)
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
pause


