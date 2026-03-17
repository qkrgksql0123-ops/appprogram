# Handwritten Digit Recognizer

A web-based application that recognizes handwritten digits (0-9) using machine learning.

## Features

- **Interactive Canvas**: Draw digits on a web-based canvas
- **Real-time Recognition**: Uses a trained neural network to recognize digits
- **Confidence Score**: Shows the confidence level of the prediction
- **Probability Distribution**: Displays the probability for each digit (0-9)
- **Responsive Design**: Works on both desktop and mobile devices

## Installation

1. Make sure you have Python 3.7+ installed

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Navigate to the project directory:
```bash
cd path/to/project_a/260317
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and go to:
```
http://localhost:5000
```

4. Draw a digit on the canvas and click "Recognize" to see the prediction!

## How It Works

1. **Drawing**: Use your mouse to draw a digit on the canvas
2. **Recognition**: Click the "Recognize" button to send the image to the backend
3. **Prediction**: The pre-trained MNIST neural network model recognizes the digit
4. **Results**: See the recognized digit with confidence score and probability distribution

## Project Structure

```
project_a/260317/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface
└── mnist_model.h5        # Trained model (created on first run)
```

## Technical Details

### Model

- **Type**: Deep Neural Network
- **Training Dataset**: MNIST (Modified National Institute of Standards and Technology)
- **Architecture**:
  - Input Layer: 28x28 pixels (flattened)
  - Hidden Layer 1: 128 neurons with ReLU activation
  - Dropout: 20%
  - Hidden Layer 2: 64 neurons with ReLU activation
  - Dropout: 20%
  - Output Layer: 10 neurons with Softmax activation (digits 0-9)

### Image Preprocessing

1. Convert drawing to grayscale
2. Invert colors (MNIST uses black background, white digit)
3. Resize to 28x28 pixels
4. Normalize pixel values (0-1 range)

## First Run

On the first run, the application will:
1. Check if `mnist_model.h5` exists
2. If not, it will train a new model on the MNIST dataset
3. Save the trained model for future use

Training may take 1-2 minutes depending on your system.

## Requirements

- Python 3.7+
- Flask
- TensorFlow
- NumPy
- OpenCV
- Pillow

See `requirements.txt` for specific versions.

## License

This project is open source and available for educational purposes.
