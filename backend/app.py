from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)
CORS(app)

# Optional: Google Vision API for better image recognition
# Set GOOGLE_VISION_API_KEY environment variable to enable
GOOGLE_VISION_API_KEY = os.environ.get('GOOGLE_VISION_API_KEY')

def recognize_item_google_vision(image_data):
    """
    Recognize items using Google Vision API (if API key is provided)
    """
    if not GOOGLE_VISION_API_KEY:
        return None

    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)

        # Call Google Vision API
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
        payload = {
            "requests": [{
                "image": {
                    "content": base64.b64encode(image_bytes).decode('utf-8')
                },
                "features": [
                    {"type": "LABEL_DETECTION", "maxResults": 10},
                    {"type": "OBJECT_LOCALIZATION", "maxResults": 10}
                ]
            }]
        }

        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if 'responses' in data and len(data['responses']) > 0:
            labels = data['responses'][0].get('labelAnnotations', [])
            objects = data['responses'][0].get('localizedObjectAnnotations', [])

            detected_items = []

            # Get object names
            for obj in objects[:3]:
                if obj.get('name'):
                    detected_items.append(obj['name'])

            # Get top labels as fallback
            for label in labels[:5]:
                if label.get('description') and label.get('score', 0) > 0.7:
                    detected_items.append(label['description'])

            if detected_items:
                return {
                    "detected_items": list(set(detected_items))[:3],  # Unique items, top 3
                    "confidence": 0.9
                }
    except Exception as e:
        print(f"Google Vision API error: {e}")

    return None

def recognize_item(image_data):
    """
    Recognize items in the image.
    Tries Google Vision API first if available, otherwise returns placeholder.
    In production, you might want to use AWS Rekognition, or a local ML model.
    """
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Try Google Vision API first
        result = recognize_item_google_vision(image_data)
        if result:
            return result

        # Fallback: Return placeholder (user will need to enter item name)
        # In a full implementation, you could use a local ML model here
        return {
            "detected_items": [],  # Empty list triggers manual input
            "confidence": 0.0,
            "requires_manual_input": True
        }
    except Exception as e:
        return {"error": str(e)}


def search_google_shopping(item_name):
    """
    Search Google Shopping for the item and extract prices
    """
    try:
        query = item_name.replace(' ', '+')
        url = f"https://www.google.com/search?tbm=shop&q={query}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        prices = []
        # Try multiple methods to extract prices
        # Method 1: Look for price patterns in text
        price_pattern = re.compile(r'[\$£€¥]\s*([\d,]+\.?\d*)')
        all_text = soup.get_text()
        matches = price_pattern.findall(all_text)

        for match in matches:
            try:
                price = float(match.replace(',', ''))
                # Filter out unrealistic prices (too low or too high)
                if 0.01 < price < 1000000:
                    prices.append(price)
            except:
                continue

        # Method 2: Look for specific price elements
        price_elements = soup.find_all(['span', 'div'], class_=re.compile(r'price', re.I))
        for elem in price_elements:
            text = elem.get_text()
            match = re.search(r'[\$£€¥]?\s*([\d,]+\.?\d*)', text)
            if match:
                try:
                    price = float(match.group(1).replace(',', ''))
                    if 0.01 < price < 1000000:
                        prices.append(price)
                except:
                    continue

        # Remove duplicates and sort
        prices = sorted(list(set(prices)))

        if len(prices) >= 3:
            # Use middle 80% to avoid outliers
            start_idx = int(len(prices) * 0.1)
            end_idx = int(len(prices) * 0.9)
            filtered_prices = prices[start_idx:end_idx]

            if filtered_prices:
                avg_price = sum(filtered_prices) / len(filtered_prices)
                min_price = min(filtered_prices)
                max_price = max(filtered_prices)
            else:
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
        elif prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
        else:
            return None

        return {
            "average_price": round(avg_price, 2),
            "min_price": round(min_price, 2),
            "max_price": round(max_price, 2),
            "price_count": len(prices),
            "prices": prices[:10]  # Return top 10 unique prices
        }
    except Exception as e:
        print(f"Error searching Google Shopping: {e}")
        return None


def search_amazon(item_name):
    """
    Alternative: Search Amazon for pricing (requires proper handling of anti-bot measures)
    """
    try:
        query = item_name.replace(' ', '+')
        url = f"https://www.amazon.com/s?k={query}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        # Note: Amazon may block simple scraping - consider using APIs like Amazon Product Advertising API
        # For demo, we'll return None and fall back to Google Shopping
        return None
    except:
        return None


@app.route('/api/scan', methods=['POST'])
def scan_item():
    """
    Main endpoint: receives image, recognizes item, and finds price
    """
    try:
        data = request.json
        image_data = data.get('image')
        item_name = data.get('item_name', None)  # Optional: if user provides item name directly

        if not image_data and not item_name:
            return jsonify({"error": "No image or item name provided"}), 400

        # If item name is provided, skip recognition
        if item_name:
            detected_item = item_name
        else:
            # Recognize item from image
            recognition_result = recognize_item(image_data)
            if "error" in recognition_result:
                return jsonify({"error": recognition_result["error"]}), 500

            # Get detected items
            detected_items = recognition_result.get("detected_items", [])

            # If no items detected or confidence is too low, return error to trigger manual input
            if not detected_items or recognition_result.get("requires_manual_input", False):
                return jsonify({
                    "status": "recognition_failed",
                    "message": "Could not automatically recognize item. Please enter the item name manually."
                }), 200

            # Use the first detected item
            detected_item = detected_items[0]

        # Search for prices
        price_info = search_google_shopping(detected_item)

        if not price_info:
            price_info = search_amazon(detected_item)

        if price_info:
            return jsonify({
                "item_name": detected_item,
                "price_info": price_info,
                "status": "success"
            })
        else:
            return jsonify({
                "item_name": detected_item,
                "price_info": None,
                "status": "no_prices_found",
                "message": "Could not find pricing information for this item"
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_price():
    """
    Alternative endpoint: search by item name directly
    """
    try:
        data = request.json
        item_name = data.get('item_name')

        if not item_name:
            return jsonify({"error": "No item name provided"}), 400

        price_info = search_google_shopping(item_name)

        if not price_info:
            price_info = search_amazon(item_name)

        if price_info:
            return jsonify({
                "item_name": item_name,
                "price_info": price_info,
                "status": "success"
            })
        else:
            return jsonify({
                "item_name": item_name,
                "price_info": None,
                "status": "no_prices_found"
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

