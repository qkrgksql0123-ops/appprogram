from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
import joblib
import os

app = Flask(__name__)

# Load or train the model
MODEL_PATH = 'digit_model.pkl'

if os.path.exists(MODEL_PATH):
    print("Loading existing model...")
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
else:
    print("Training a new model...")
    # Load MNIST-like digits dataset (8x8 images)
    digits_data = load_digits()
    X = digits_data.data / 16.0  # Normalize
    y = digits_data.target

    # Create and train model
    model = MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42,
        verbose=1
    )

    print("Training model...")
    model.fit(X, y)

    # Save model
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved!")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Process the drawn image and predict the digit"""
    try:
        # Get image data from request
        data = request.json
        image_data = data['image']

        # Decode base64 image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes)).convert('L')

        # Convert to numpy array
        img_array = np.array(image)

        # Invert colors
        img_array = 255 - img_array

        # Resize to 28x28
        img_resized = cv2.resize(img_array, (28, 28))

        # Resize to 8x8 to match training data
        img_8x8 = cv2.resize(img_array, (8, 8))

        # Normalize
        img_normalized = img_8x8.astype('float32') / 16.0

        # Reshape for model input
        img_input = img_normalized.reshape(1, -1)

        # Make prediction
        digit = int(model.predict(img_input)[0])
        probabilities = model.predict_proba(img_input)[0]
        confidence = float(np.max(probabilities)) * 100

        # Return result
        return jsonify({
            'success': True,
            'digit': digit,
            'confidence': confidence,
            'probabilities': probabilities.tolist()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
