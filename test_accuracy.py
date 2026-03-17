import numpy as np
from sklearn.datasets import load_digits
from sklearn.neural_network import MLPClassifier
import joblib
import os

# Load model
MODEL_PATH = 'digit_model.pkl'

if not os.path.exists(MODEL_PATH):
    print("모델이 없습니다. digit_recognizer.py를 먼저 실행해주세요.")
    exit()

print("모델 로딩 중...")
model = joblib.load(MODEL_PATH)

print("테스트 데이터셋 로딩 중...")
# Load digits dataset
digits_data = load_digits()
X = digits_data.data / 16.0  # Normalize
y = digits_data.target

# Split data for testing (using last 20% of data)
split_idx = int(len(X) * 0.8)
X_train = X[:split_idx]
y_train = y[:split_idx]
X_test = X[split_idx:]
y_test = y[split_idx:]

print(f"\n테스트 샘플 수: {len(X_test)}")

# Calculate accuracy
train_accuracy = model.score(X_train, y_train) * 100
test_accuracy = model.score(X_test, y_test) * 100

print("\n" + "="*50)
print("모델 정확도 측정 결과")
print("="*50)
print(f"훈련 정확도: {train_accuracy:.2f}%")
print(f"테스트 정확도: {test_accuracy:.2f}%")
print("="*50)

# Detailed analysis
print("\n숫자별 정확도:")
print("-"*50)

from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, digits=3))

print("\n혼동 행렬 (Confusion Matrix):")
print(confusion_matrix(y_test, y_pred))
