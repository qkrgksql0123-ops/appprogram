# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 설명 (한국어)

이 프로젝트는 손글씨로 쓴 숫자(0-9)를 인식하는 AI 애플리케이션입니다. 사용자가 그린 숫자를 머신러닝 모델이 인식하고, 사용자가 정답을 입력하면 그 데이터로 모델을 학습시켜 정확도를 높입니다.
Tkinter(데스크톱)와 Flask(웹) 두 가지 인터페이스를 모두 지원하며, scikit-learn의 MLPClassifier를 사용해 97% 이상의 정확도를 달성했습니다.

## 오늘 배운 것 (한국어)

Canvas 그리기, 이미지 전처리, 머신러닝 모델 학습 및 재학습을 구현했습니다.
사용자 피드백으로 모델을 지속적으로 개선하는 Active Learning 개념과 Tkinter/Flask를 활용한 GUI/웹 개발을 경험했습니다.

## Project Overview

A handwritten digit recognition application with a Tkinter GUI and active learning capability. The application allows users to draw digits (0-9), recognize them using a pre-trained model, and improve accuracy by providing corrected labels for retraining.

**Language**: All code comments and strings are in English except the GUI which uses Korean.

## Running the Application

### Main Application (Tkinter GUI with Learning)
```bash
python digit_recognizer.py
```

This launches the active learning interface where users can:
1. Draw a digit on canvas
2. Click "인식" (Recognize) to see prediction
3. Enter actual digit in input field
4. Click "학습에 추가" (Add to Learning) to save training example
5. Click "모델 재학습" (Retrain Model) to improve the model with collected data

### Testing Model Accuracy
```bash
python test_accuracy.py
```

Runs evaluation on test set using last 20% of MNIST dataset. Shows:
- Train/test accuracy percentages
- Per-digit precision/recall/f1-scores
- Confusion matrix

### Legacy Web Application (Flask)
```bash
python app.py
```
Deprecated Flask web interface (accessible at http://localhost:5000)

## Architecture & Key Components

### Model Training & Persistence
- **Main Model**: `digit_model.pkl` - scikit-learn MLPClassifier with architecture (256, 128) hidden layers
- **Custom Data**: `custom_data.npz` - User-provided training examples (arrays X and y)
- **Initial Training**: Uses sklearn.datasets.load_digits() (1797 samples, 8x8 pixels)
- **Retraining**: Combines MNIST dataset + accumulated custom_data

### Image Preprocessing Pipeline
1. Convert PIL image to grayscale
2. Invert colors (MNIST convention: white digit on black background)
3. Resize to 8x8 pixels (matches MNIST feature size)
4. Normalize to 0-16 range (divide by 16.0)
5. Flatten to 64 features for model input

### Model Architecture
- **Type**: MLPClassifier (scikit-learn)
- **Hidden Layers**: (256, 128) with ReLU activation
- **Solver**: Adam optimizer
- **Max Iterations**: 500
- **Early Stopping**: Enabled with validation_fraction=0.1
- **Learning Rate**: 0.001
- **Output**: 10 neurons (digits 0-9)

### Key Data Structures
- `model`: Global MLPClassifier instance (loaded/trained at startup)
- `custom_X`, `custom_y`: Lists accumulating user-provided training examples
- Canvas image: PIL Image (400x300 for drawing, resized to 8x8 for model)

## Important Implementation Details

### Retraining Process
When "모델 재학습" is clicked:
1. Combines original MNIST data with accumulated custom_data
2. Creates new MLPClassifier with same architecture
3. Trains on combined dataset
4. Saves updated model to digit_model.pkl
5. Custom data persists in custom_data.npz for next session

### Image Dimensions
- Canvas display: 400×300 pixels (for user drawing)
- Canvas stored: PIL Image same size
- Model input: 8×8 pixels (after cv2.resize)
- Feature vector: 64 elements (8×8 flattened)

### File Persistence
- `digit_model.pkl`: Trained model (joblib format)
- `custom_data.npz`: NumPy compressed archive with keys 'X' (images) and 'y' (labels)
- Files saved in same directory as script

## GUI Structure (Tkinter)

Three main sections with step-by-step UX:
1. **Canvas Section**: Draw digit
2. **Input Section**: Enter actual digit (0-9)
3. **Result Section**: Shows prediction, confidence, probability distribution

Four action buttons: "인식" (Recognize), "학습에 추가" (Add to Learning), "모델 재학習" (Retrain), "지우기" (Clear)

## Dependencies

Core ML libraries:
- `scikit-learn`: MLPClassifier, load_digits, classification_report, confusion_matrix
- `numpy`: Array operations
- `opencv-python`: Image resizing (cv2.resize)
- `Pillow`: Image creation and drawing (Image, ImageDraw)
- `joblib`: Model serialization

GUI:
- `tkinter`: Built-in Python GUI framework

## Known Constraints & Design Decisions

1. **8×8 image size**: Chosen to match MNIST dataset, though this limits handwriting detail. Could be upgraded to 28×28 if accuracy becomes critical bottleneck.

2. **Retraining blocks UI**: Model retraining runs synchronously and freezes GUI during training (~1-2 minutes). Consider adding threading if responsiveness becomes issue.

3. **No validation split on custom data**: Combined MNIST+custom data uses validation_fraction=0.1 on merged set. Could add separate validation for custom-only accuracy tracking.

4. **Global model state**: `model`, `custom_X`, `custom_y` are module-level globals. Works for single-window app but would need refactoring for multi-instance scenarios.

## Future Enhancement Considerations

- Use 28×28 images instead of 8×8 for higher fidelity
- Add threading to prevent UI blocking during retraining
- Track separate metrics for MNIST vs custom-trained accuracy
- Add visual feedback (progress bar) during model retraining
- Persist accuracy metrics across sessions
