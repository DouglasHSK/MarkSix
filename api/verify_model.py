import tensorflow as tf
import os

try:
    print("Attempting to load model...")
    model = tf.keras.models.load_model('data/marksix_model.keras', compile=False)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    print(f"File exists: {os.path.exists('data/marksix_model.keras')}")
    print(f"File size: {os.path.getsize('data/marksix_model.keras')} bytes")