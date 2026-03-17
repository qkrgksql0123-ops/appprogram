from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
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
CORS(app)

# Model configuration
MODEL_PATH = 'digit_model_web.pkl'
CUSTOM_DATA_PATH = 'custom_data_web.npz'

# Load or train the model
print("모델 로딩 중...")
model = None

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("기존 모델 로드 완료!")
    except:
        print("모델 로드 실패, 새로 학습합니다...")
        model = None

if model is None:
    print("새로운 모델을 학습 중...")

    # Load digits dataset
    digits_data = load_digits()
    X = digits_data.data / 16.0
    y = digits_data.target

    # Create and train model
    model = MLPClassifier(
        hidden_layer_sizes=(256, 128),
        activation='relu',
        solver='adam',
        max_iter=500,
        random_state=42,
        verbose=0,
        early_stopping=True,
        validation_fraction=0.1,
        learning_rate_init=0.001
    )

    print("모델 학습 중...")
    model.fit(X, y)

    # Save model
    joblib.dump(model, MODEL_PATH)
    print("모델 학습 완료!")

# Load custom training data if exists
custom_X = []
custom_y = []

if os.path.exists(CUSTOM_DATA_PATH):
    try:
        data = np.load(CUSTOM_DATA_PATH)
        custom_X = list(data['X'])
        custom_y = list(data['y'])
        print(f"커스텀 학습 데이터 로드 완료! ({len(custom_y)}개 샘플)")
    except:
        print("커스텀 데이터 로드 실패")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('web_index.html', custom_data_count=len(custom_y))

@app.route('/predict', methods=['POST'])
def predict():
    """Predict digit from image"""
    try:
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

        # Resize to 8x8
        img_resized = cv2.resize(img_array, (8, 8))

        # Normalize
        img_normalized = img_resized.astype('float32') / 16.0

        # Flatten
        img_flat = img_normalized.flatten()

        # Make prediction
        digit = int(model.predict(img_flat.reshape(1, -1))[0])
        probabilities = model.predict_proba(img_flat.reshape(1, -1))[0]
        confidence = float(np.max(probabilities)) * 100

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

@app.route('/add_to_training', methods=['POST'])
def add_to_training():
    """Add image to training data"""
    try:
        data = request.json
        image_data = data['image']
        digit_label = int(data['label'])

        # Validate digit
        if digit_label < 0 or digit_label > 9:
            return jsonify({
                'success': False,
                'error': '숫자는 0-9 사이여야 합니다'
            }), 400

        # Decode base64 image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes)).convert('L')

        # Convert to numpy array
        img_array = np.array(image)

        # Invert colors
        img_array = 255 - img_array

        # Resize to 8x8
        img_resized = cv2.resize(img_array, (8, 8))

        # Normalize
        img_normalized = img_resized.astype('float32') / 16.0

        # Flatten
        img_flat = img_normalized.flatten()

        # Add to custom data
        custom_X.append(img_flat)
        custom_y.append(digit_label)

        # Save custom data
        np.savez(CUSTOM_DATA_PATH, X=np.array(custom_X), y=np.array(custom_y))

        return jsonify({
            'success': True,
            'message': f'숫자 {digit_label}이(가) 학습 데이터에 추가되었습니다!',
            'total_samples': len(custom_y)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain model with custom data"""
    try:
        global model

        if len(custom_y) == 0:
            return jsonify({
                'success': False,
                'error': '학습 데이터가 없습니다'
            }), 400

        # Load MNIST data
        digits_data = load_digits()
        X_mnist = digits_data.data / 16.0
        y_mnist = digits_data.target

        # Combine with custom data
        X_combined = np.vstack([X_mnist, np.array(custom_X)])
        y_combined = np.hstack([y_mnist, np.array(custom_y)])

        # Retrain model
        model = MLPClassifier(
            hidden_layer_sizes=(256, 128),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42,
            verbose=0,
            early_stopping=True,
            validation_fraction=0.1,
            learning_rate_init=0.001
        )

        print("모델 재학습 중...")
        model.fit(X_combined, y_combined)

        # Save retrained model
        joblib.dump(model, MODEL_PATH)

        return jsonify({
            'success': True,
            'message': '모델 재학습이 완료되었습니다!'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/get_status', methods=['GET'])
def get_status():
    """Get current training data count"""
    return jsonify({
        'success': True,
        'custom_data_count': len(custom_y)
    })

if __name__ == '__main__':
    print("\n웹 앱 실행 중...\n")
    print("http://localhost:5000 에서 접속하세요\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
