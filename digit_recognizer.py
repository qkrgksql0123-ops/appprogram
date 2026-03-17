import tkinter as tk
from tkinter import messagebox
import numpy as np
import cv2
from PIL import Image, ImageDraw
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
import joblib
import os

# Load or train the model
MODEL_PATH = 'digit_model.pkl'
CUSTOM_DATA_PATH = 'custom_data.npz'

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
    print("(이 과정은 2-3분 소요됩니다)")

    # Load digits dataset
    digits_data = load_digits()
    X = digits_data.data / 16.0  # Normalize to 0-1
    y = digits_data.target

    # Create and train model with larger architecture
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

class DigitRecognizer:
    def __init__(self, root):
        self.root = root
        self.root.title("손글씨 숫자 인식기 (학습 모드)")
        self.root.geometry("600x850")
        self.root.configure(bg='#f0f0f0')

        # Title
        title_frame = tk.Frame(root, bg='#667eea')
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="손글씨 숫자 인식기 (학습 모드)",
            font=('Arial', 18, 'bold'),
            bg='#667eea',
            fg='white',
            pady=12
        )
        title_label.pack()

        # Main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Canvas label
        canvas_label = tk.Label(
            main_frame,
            text="1. 숫자(0-9)를 아래에 그려주세요:",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0'
        )
        canvas_label.pack(pady=(0, 8), anchor=tk.W)

        # Create canvas for drawing
        self.canvas = tk.Canvas(
            main_frame,
            bg='white',
            width=400,
            height=300,
            cursor='cross',
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.pack(pady=8)

        # Bind mouse events
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<ButtonRelease-1>', self.end_draw)

        # Create PIL image for better drawing
        self.image = Image.new('RGB', (400, 300), 'white')
        self.draw_tool = ImageDraw.Draw(self.image)

        # Input frame
        input_frame = tk.LabelFrame(
            main_frame,
            text="2. 실제 숫자를 입력해주세요",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#333',
            padx=10,
            pady=10
        )
        input_frame.pack(pady=10, fill=tk.X)

        input_label = tk.Label(
            input_frame,
            text="실제 숫자 (0-9):",
            font=('Arial', 10),
            bg='#f0f0f0'
        )
        input_label.pack(side=tk.LEFT, padx=5)

        self.digit_input = tk.Entry(
            input_frame,
            font=('Arial', 14, 'bold'),
            width=5,
            justify=tk.CENTER
        )
        self.digit_input.pack(side=tk.LEFT, padx=5)
        self.digit_input.focus()

        # Button frame
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10, fill=tk.X)

        # Recognize button
        recognize_btn = tk.Button(
            button_frame,
            text="인식",
            command=self.recognize_digit,
            bg='#667eea',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        )
        recognize_btn.pack(side=tk.LEFT, padx=3)

        # Learn button
        learn_btn = tk.Button(
            button_frame,
            text="학습에 추가",
            command=self.add_to_learning,
            bg='#51cf66',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        )
        learn_btn.pack(side=tk.LEFT, padx=3)

        # Retrain button
        retrain_btn = tk.Button(
            button_frame,
            text="모델 재학습",
            command=self.retrain_model,
            bg='#ffa94d',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        )
        retrain_btn.pack(side=tk.LEFT, padx=3)

        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="지우기",
            command=self.clear_canvas,
            bg='#ff6b6b',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=8
        )
        clear_btn.pack(side=tk.LEFT, padx=3)

        # Result frame
        result_frame = tk.LabelFrame(
            main_frame,
            text="3. 인식 결과",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#333',
            padx=15,
            pady=12
        )
        result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Prediction result
        self.prediction_label = tk.Label(
            result_frame,
            text="인식된 숫자: -",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#667eea'
        )
        self.prediction_label.pack(pady=5)

        # Confidence label
        self.confidence_label = tk.Label(
            result_frame,
            text="신뢰도: 0%",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666'
        )
        self.confidence_label.pack(pady=3)

        # Status label
        self.status_label = tk.Label(
            result_frame,
            text=f"학습 데이터: {len(custom_y)}개",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#999'
        )
        self.status_label.pack(pady=5)

        # Probability text
        self.probability_text = tk.Label(
            result_frame,
            text="결과가 표시될 곳입니다",
            font=('Courier', 8),
            bg='white',
            fg='#666',
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            bd=1,
            padx=10,
            pady=8
        )
        self.probability_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        self.last_x = None
        self.last_y = None

    def start_draw(self, event):
        """그리기 시작"""
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        """캔버스에 그리기"""
        if self.last_x and self.last_y:
            # Draw on tkinter canvas
            self.canvas.create_line(
                self.last_x, self.last_y,
                event.x, event.y,
                fill='black',
                width=4,
                capstyle=tk.ROUND,
                smooth=tk.TRUE
            )

            # Draw on PIL image
            self.draw_tool.line(
                [(self.last_x, self.last_y), (event.x, event.y)],
                fill='black',
                width=4
            )

        self.last_x = event.x
        self.last_y = event.y

    def end_draw(self, event):
        """그리기 종료"""
        self.last_x = None
        self.last_y = None

    def preprocess_image(self):
        """그린 이미지를 모델 형식으로 변환"""
        try:
            # Convert PIL image to numpy array
            img_array = np.array(self.image.convert('L'))

            # Invert colors (MNIST uses white on black)
            img_array = 255 - img_array

            # Resize to 8x8 to match MNIST dataset
            img_resized = cv2.resize(img_array, (8, 8))

            # Normalize to 0-16 range to match MNIST
            img_normalized = img_resized.astype('float32') / 16.0

            # Flatten to 1D array (64 features)
            img_flat = img_normalized.flatten()

            return img_flat
        except Exception as e:
            print(f"전처리 오류: {e}")
            raise

    def recognize_digit(self):
        """손글씨 숫자 인식"""
        try:
            # Check if model is loaded
            if model is None:
                messagebox.showerror("오류", "모델이 로드되지 않았습니다.")
                return

            # Preprocess image
            img_processed = self.preprocess_image()

            # Make prediction
            digit = int(model.predict(img_processed.reshape(1, -1))[0])
            probabilities = model.predict_proba(img_processed.reshape(1, -1))[0]
            confidence = float(np.max(probabilities)) * 100

            # Update result labels
            self.prediction_label.config(text=f"인식된 숫자: {digit}")
            self.confidence_label.config(text=f"신뢰도: {confidence:.1f}%")

            # Display probabilities
            prob_text = ""
            for i, prob in enumerate(probabilities):
                percentage = prob * 100
                bar_length = int(percentage / 5)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                prob_text += f"{i}: {bar} {percentage:5.1f}%\n"

            self.probability_text.config(text=prob_text.strip())

        except Exception as e:
            messagebox.showerror("오류", f"인식 중 오류가 발생했습니다:\n{str(e)}")

    def add_to_learning(self):
        """현재 그림을 학습 데이터에 추가"""
        try:
            # Get the entered digit
            digit_str = self.digit_input.get().strip()

            # Validate input
            if not digit_str or len(digit_str) != 1:
                messagebox.showerror("오류", "0-9 중 한 개의 숫자만 입력해주세요!")
                return

            try:
                digit = int(digit_str)
                if digit < 0 or digit > 9:
                    raise ValueError()
            except:
                messagebox.showerror("오류", "0-9 중 한 개의 숫자만 입력해주세요!")
                return

            # Preprocess image
            img_processed = self.preprocess_image()

            # Add to custom data
            custom_X.append(img_processed)
            custom_y.append(digit)

            # Save custom data
            np.savez(CUSTOM_DATA_PATH, X=np.array(custom_X), y=np.array(custom_y))

            # Update status
            self.status_label.config(text=f"학습 데이터: {len(custom_y)}개")

            messagebox.showinfo("성공", f"숫자 {digit}이(가) 학습 데이터에 추가되었습니다!\n(총 {len(custom_y)}개)")

            # Clear inputs
            self.clear_canvas()

        except Exception as e:
            messagebox.showerror("오류", f"학습 데이터 추가 중 오류: {str(e)}")

    def retrain_model(self):
        """수집한 데이터로 모델 재학습"""
        try:
            if len(custom_y) == 0:
                messagebox.showerror("오류", "학습 데이터가 없습니다. 먼저 데이터를 추가해주세요!")
                return

            # Confirm retrain
            result = messagebox.askyesno(
                "모델 재학습",
                f"현재 {len(custom_y)}개의 학습 데이터로 모델을 재학습하시겠습니까?\n(약 1-2분 소요)"
            )

            if not result:
                return

            messagebox.showinfo("재학습", "모델 재학습을 시작합니다. 잠깐만 기다려주세요...")

            # Load original MNIST data
            digits_data = load_digits()
            X_mnist = digits_data.data / 16.0
            y_mnist = digits_data.target

            # Add custom data
            X_combined = np.vstack([X_mnist, np.array(custom_X)])
            y_combined = np.hstack([y_mnist, np.array(custom_y)])

            # Retrain model
            global model
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

            messagebox.showinfo("완료", "모델 재학습이 완료되었습니다!\n이제 더 정확한 인식이 가능합니다.")

        except Exception as e:
            messagebox.showerror("오류", f"재학습 중 오류가 발생했습니다:\n{str(e)}")

    def clear_canvas(self):
        """캔버스 지우기"""
        self.canvas.delete('all')
        self.image = Image.new('RGB', (400, 300), 'white')
        self.draw_tool = ImageDraw.Draw(self.image)
        self.prediction_label.config(text="인식된 숫자: -")
        self.confidence_label.config(text="신뢰도: 0%")
        self.digit_input.delete(0, tk.END)
        self.digit_input.focus()
        self.probability_text.config(text="결과가 표시될 곳입니다")

# Run application
if __name__ == "__main__":
    print("\nGUI 실행 중...\n")
    root = tk.Tk()
    app = DigitRecognizer(root)
    root.mainloop()
