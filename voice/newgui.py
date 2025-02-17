import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import sounddevice as sd
import numpy as np
import tensorflow as tf
import librosa

# Load the trained model
model = tf.keras.models.load_model('model.h5')

# Function to record audio
def record_audio(duration=5, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until the recording is finished
    print("Recording finished")
    return np.squeeze(recording)

# Function to convert audio to MFCC
def audio_to_mfcc(audio_data, sr=44100, n_mfcc=13):
    mfcc = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=n_mfcc)
    mfcc = np.mean(mfcc.T, axis=0)
    return mfcc

# Function to predict emotion from audio
def predict_emotion(audio_data):
    mfcc_features = audio_to_mfcc(audio_data)
    # Reshape to match model input shape (1, time_steps, 1)
    mfcc_features = mfcc_features.reshape(1, -1, 1)
    prediction = model.predict(mfcc_features)
    emotion = np.argmax(prediction)
    return emotion

# Dictionary to map emotion index to emotion label
emotion_labels = {0: 'Angry', 1: 'Calm', 2: 'Happy', 3: 'Sad'}

# Function to handle recording and prediction
def handle_recording():
    audio_data = record_audio()
    emotion_index = predict_emotion(audio_data)
    emotion = emotion_labels[emotion_index]
    messagebox.showinfo("Prediction", f"Predicted Emotion: {emotion}")

# GUI setup
root = tk.Tk()
root.title("Emotion Recognition")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to a quarter of the screen size
window_width = screen_width // 2
window_height = screen_height // 2
root.geometry(f"{window_width}x{window_height}")

# Load background image
bg_image_path = "../background.png"  # Replace with the path to your background image
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((window_width, window_height), Image.ANTIALIAS)
bg_image = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Create a frame for the content to be placed on top of the background
frame = tk.Frame(root, bg='white', bd=5)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Record button
record_button = tk.Button(frame, text="Record and Predict", command=lambda: threading.Thread(target=handle_recording).start())
record_button.pack(pady=20)

# Run the GUI loop
root.mainloop()
