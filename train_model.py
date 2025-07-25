import sqlite3
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Reshape

# Function to load data from the database
def load_data():
    conn = sqlite3.connect('marksix.db')
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
def train_model():
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
    model.fit(X, y, epochs=200, verbose=1)

    # Save the model and the scaler
    model.save('marksix_model.h5')
    np.save('scaler_params.npy', {'min': scaler.min_, 'scale': scaler.scale_})

    print("Model training complete and saved as marksix_model.h5")

if __name__ == '__main__':
    train_model()