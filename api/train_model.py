import sqlite3
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Reshape
import argparse

# Function to load data from the database
def load_data():
    conn = sqlite3.connect('data/marksix.db')
    cursor = conn.cursor()
    cursor.execute("SELECT no1, no2, no3, no4, no5, no6 FROM results ORDER BY draw_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return np.array(rows)

# Function to create sequences for the LSTM model
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Main function to train the model
def train_model(epochs, device):
    # Load and preprocess the data
    data = load_data()
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Create sequences
    seq_length = 10
    X, y = create_sequences(data_scaled, seq_length)

    # Build the LSTM model
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(seq_length, 6)),
        Dense(6)
    ])
    model.compile(optimizer='adam', loss='mse')

    # Train the model
    device_name = '/GPU:0' if device == 'gpu' else '/CPU:0'
    with tf.device(device_name):
        model.fit(X, y, epochs=epochs, verbose=1)

    # Save the model and the scaler
    model.save('data/marksix_model.keras')
    np.save('data/scaler_params.npy', {'min': scaler.min_, 'scale': scaler.scale_})

    print("Model training complete and saved as marksix_model.keras")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train the Mark Six prediction model.')
    parser.add_argument('--epochs', type=int, default=2000, help='Number of epochs to train the model.')
    parser.add_argument('--device', type=str, default='gpu', choices=['gpu', 'cpu'], help='Device to use for training (gpu or cpu).')
    args = parser.parse_args()

    train_model(args.epochs, args.device)