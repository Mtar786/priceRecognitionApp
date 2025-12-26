const API_URL = 'http://localhost:5000/api';

let stream = null;
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let preview = document.getElementById('preview');
let previewContainer = document.getElementById('preview-container');

// Elements
const startCameraBtn = document.getElementById('start-camera-btn');
const captureBtn = document.getElementById('capture-btn');
const uploadBtn = document.getElementById('upload-btn');
const fileInput = document.getElementById('file-input');
const searchBtn = document.getElementById('search-btn');
const retakeBtn = document.getElementById('retake-btn');
const searchInputContainer = document.getElementById('search-input-container');
const itemNameInput = document.getElementById('item-name-input');
const submitSearchBtn = document.getElementById('submit-search-btn');
const resultsSection = document.getElementById('results-section');
const loading = document.getElementById('loading');
const resultCard = document.getElementById('result-card');
const itemNameDisplay = document.getElementById('item-name-display');
const priceInfo = document.getElementById('price-info');
const errorMessage = document.getElementById('error-message');

// Start camera
startCameraBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment' // Use back camera on mobile
            }
        });
        video.srcObject = stream;
        video.style.display = 'block';
        previewContainer.style.display = 'none';
        startCameraBtn.style.display = 'none';
        captureBtn.style.display = 'inline-block';
        hideError();
    } catch (error) {
        showError('Could not access camera. Please check permissions.');
        console.error('Camera error:', error);
    }
});

// Capture photo
captureBtn.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    // Stop camera stream
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    // Show preview
    preview.src = canvas.toDataURL('image/jpeg', 0.8);
    video.style.display = 'none';
    previewContainer.style.display = 'block';
    captureBtn.style.display = 'none';
    startCameraBtn.style.display = 'inline-block';

    // Process image
    processImage(canvas.toDataURL('image/jpeg', 0.8));
});

// Retake photo
retakeBtn.addEventListener('click', () => {
    previewContainer.style.display = 'none';
    startCameraBtn.click();
});

// Upload image
uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            preview.src = event.target.result;
            video.style.display = 'none';
            previewContainer.style.display = 'block';
            captureBtn.style.display = 'none';
            startCameraBtn.style.display = 'inline-block';
            processImage(event.target.result);
        };
        reader.readAsDataURL(file);
    }
});

// Search by name button
searchBtn.addEventListener('click', () => {
    searchInputContainer.style.display = searchInputContainer.style.display === 'none' ? 'flex' : 'none';
    itemNameInput.focus();
});

// Submit search
submitSearchBtn.addEventListener('click', () => {
    const itemName = itemNameInput.value.trim();
    if (itemName) {
        searchByItemName(itemName);
    } else {
        showError('Please enter an item name');
    }
});

itemNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        submitSearchBtn.click();
    }
});

// Process image and find price
async function processImage(imageData) {
    showLoading();
    hideError();

    try {
        const response = await fetch(`${API_URL}/scan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();
        hideLoading();

        if (data.error) {
            showError(data.error);
            return;
        }

        if (data.status === 'success' && data.price_info) {
            displayResults(data);
        } else if (data.status === 'recognition_failed') {
            // If recognition failed, ask user to enter item name
            showError(data.message || 'Could not automatically recognize item. Please enter the item name manually.');
            searchInputContainer.style.display = 'flex';
            itemNameInput.focus();
        } else {
            // If recognition failed, ask user to enter item name
            showError('Could not automatically recognize item. Please enter the item name manually.');
            searchInputContainer.style.display = 'flex';
            itemNameInput.focus();
        }
    } catch (error) {
        hideLoading();
        showError('Error connecting to server. Make sure the backend is running on http://localhost:5000');
        console.error('Error:', error);
    }
}

// Search by item name
async function searchByItemName(itemName) {
    showLoading();
    hideError();

    try {
        const response = await fetch(`${API_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ item_name: itemName })
        });

        const data = await response.json();
        hideLoading();

        if (data.error) {
            showError(data.error);
            return;
        }

        if (data.status === 'success' && data.price_info) {
            displayResults(data);
        } else {
            showError('No prices found for this item. Try a different search term.');
        }
    } catch (error) {
        hideLoading();
        showError('Error connecting to server. Make sure the backend is running on http://localhost:5000');
        console.error('Error:', error);
    }
}

// Display results
function displayResults(data) {
    resultsSection.style.display = 'block';
    itemNameDisplay.textContent = data.item_name || 'Unknown Item';

    const priceInfoData = data.price_info;
    let html = `
        <div class="price-card">
            <div class="label">Average Price</div>
            <div class="value">$${priceInfoData.average_price.toFixed(2)}</div>
        </div>
        <div class="price-card">
            <div class="label">Lowest Price</div>
            <div class="value">$${priceInfoData.min_price.toFixed(2)}</div>
        </div>
        <div class="price-card">
            <div class="label">Highest Price</div>
            <div class="value">$${priceInfoData.max_price.toFixed(2)}</div>
        </div>
    `;

    if (priceInfoData.prices && priceInfoData.prices.length > 0) {
        html += `
            <div class="price-list">
                <h3>Sample Prices Found (${priceInfoData.price_count} total)</h3>
                <ul>
                    ${priceInfoData.prices.map(price => `<li>$${price.toFixed(2)}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    priceInfo.innerHTML = html;

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// UI helper functions
function showLoading() {
    loading.style.display = 'block';
    resultCard.style.display = 'none';
    resultsSection.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
    resultCard.style.display = 'block';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function hideError() {
    errorMessage.style.display = 'none';
}

