# 💰 PriceFinder

A web application that allows users to scan items and find their prices by searching online shopping platforms. The app recognizes items from images (with optional Google Vision API) and retrieves pricing information from Google Shopping.

## Features

- 📷 **Camera Scanning**: Capture items using your device's camera
- 📁 **Image Upload**: Upload images from your device
- 🔍 **Manual Search**: Search for prices by item name
- 💵 **Price Lookup**: Automatically finds average, minimum, and maximum prices
- 🎨 **Modern UI**: Beautiful, responsive interface
- 🌐 **Cross-platform**: Works on desktop and mobile browsers

## Project Structure

```
priceFinder/
├── backend/
│   ├── app.py              # Flask backend server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── styles.css         # Styling
│   └── app.js            # Frontend JavaScript
└── README.md             # This file
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A modern web browser with camera support

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up Google Vision API for better image recognition:
   - Get a Google Cloud API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Vision API for your project
   - Set the environment variable:
   ```bash
   # On Windows:
   set GOOGLE_VISION_API_KEY=your_api_key_here

   # On macOS/Linux:
   export GOOGLE_VISION_API_KEY=your_api_key_here
   ```

5. Run the backend server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Frontend Setup

1. Open the `frontend/index.html` file in a web browser, OR

2. For better development experience, use a local server:
```bash
# Using Python 3:
cd frontend
python -m http.server 8000

# Using Node.js (if you have it installed):
npx http-server frontend -p 8000
```

3. Open your browser and navigate to:
   - `http://localhost:8000` (if using a server)
   - Or open `frontend/index.html` directly in your browser

## Usage

1. **Start the backend server** (see Backend Setup above)

2. **Open the frontend** in your browser

3. **Scan an item**:
   - Click "Start Camera" to use your device camera
   - Or click "Upload Image" to upload a photo
   - Or click "Search by Name" to manually enter an item name

4. **View results**: The app will display:
   - Average price
   - Lowest price
   - Highest price
   - Sample prices found

## How It Works

1. **Image Recognition**:
   - If Google Vision API key is provided, uses Google's Vision API for object detection
   - Otherwise, prompts user to enter item name manually

2. **Price Lookup**:
   - Searches Google Shopping for the detected/entered item name
   - Extracts prices from search results
   - Calculates average, minimum, and maximum prices

## API Endpoints

- `POST /api/scan` - Scan image and find price
  - Body: `{ "image": "base64_encoded_image" }`

- `POST /api/search` - Search by item name
  - Body: `{ "item_name": "item name" }`

- `GET /health` - Health check endpoint

## Limitations

- Image recognition without Google Vision API requires manual item name input
- Price scraping from Google Shopping may be affected by changes in Google's HTML structure
- Some websites may block automated scraping requests
- The app is for demonstration purposes and should comply with websites' terms of service

## Future Improvements

- [ ] Integrate with more price comparison APIs
- [ ] Add support for barcode/QR code scanning
- [ ] Implement local ML model for image recognition (no API key needed)
- [ ] Add price history tracking
- [ ] Support multiple currencies
- [ ] Add product reviews and ratings
- [ ] Implement caching for faster responses

## Troubleshooting

**Backend won't start:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is already in use

**Camera not working:**
- Ensure you've granted camera permissions in your browser
- Try using HTTPS (some browsers require secure context for camera access)

**No prices found:**
- Try being more specific with item names
- Check your internet connection
- Google Shopping may have changed their HTML structure

**CORS errors:**
- Make sure the backend is running and accessible
- Check that `flask-cors` is installed
- Verify the API_URL in `frontend/app.js` matches your backend URL

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.


