# Quick Start Guide - PriceFinder

## Windows Quick Start (Easiest Method)

### Step 1: Start the Backend Server

**Option A - Using the batch file (Easiest):**
1. Double-click `start_backend.bat` in the main folder
2. Wait for it to install dependencies and start the server
3. You should see: `Running on http://127.0.0.1:5000`

**Option B - Manual method:**
1. Open PowerShell or Command Prompt
2. Navigate to the project folder:
   ```powershell
   cd C:\Users\fayyi\Downloads\priceFinder
   ```
3. Go to backend folder:
   ```powershell
   cd backend
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the server:
   ```powershell
   python app.py
   ```
6. You should see: `Running on http://127.0.0.1:5000`

**Keep this window open!** The backend must be running for the app to work.

### Step 2: Open the Frontend

1. Navigate to the `frontend` folder
2. Double-click `index.html` to open it in your browser
3. Or open your browser and go to: `file:///C:/Users/fayyi/Downloads/priceFinder/frontend/index.html`

### Step 3: Use the App!

1. Click **"Start Camera"** to scan an item (allow camera permissions when prompted)
2. Or click **"Upload Image"** to upload a photo
3. Or click **"Search by Name"** to manually search for an item

The app will search for prices and display results!

---

## Troubleshooting

**Backend won't start?**
- Make sure Python is installed: `python --version`
- Try: `pip install flask flask-cors pillow requests beautifulsoup4 lxml`

**Can't see the frontend?**
- Make sure the backend is running first
- Try using a simple HTTP server:
  ```powershell
  cd frontend
  python -m http.server 8000
  ```
  Then open: http://localhost:8000

**Camera not working?**
- Make sure you've granted camera permissions in your browser
- Try uploading an image instead

**No prices found?**
- The app needs an internet connection
- Try being more specific with item names (e.g., "iPhone 15 Pro" instead of just "iPhone")

---

## What You'll See

When working correctly:
- Backend: Shows `Running on http://127.0.0.1:5000` and logs requests
- Frontend: Shows the PriceFinder interface where you can scan/search items

