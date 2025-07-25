import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import sqlite3

# Function to load the last sequence of data
def load_last_sequence():
    conn = sqlite3.connect('marksix.db')
    cursor = conn.cursor()
    cursor.execute("SELECT no1, no2, no3, no4, no5, no6 FROM results ORDER BY draw_date DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return np.array(rows)

# Main function to make a prediction
def predict_next_draws(num_predictions=10):
    # Load the trained model and scaler
    model = tf.keras.models.load_model('marksix_model.h5', compile=False)
    scaler_params = np.load('scaler_params.npy', allow_pickle=True).item()
    scaler = MinMaxScaler()
    scaler.min_ = scaler_params['min']
    scaler.scale_ = scaler_params['scale']

    # Load the last sequence of data
    last_sequence = load_last_sequence()
    last_sequence_scaled = scaler.transform(last_sequence)

    predictions_scaled = []
    current_sequence = last_sequence_scaled.reshape((1, 10, 6))

    for _ in range(num_predictions):
        # Make a prediction
        next_prediction_scaled = model.predict(current_sequence, verbose=0)
        predictions_scaled.append(next_prediction_scaled[0])
        
        # Update the sequence for the next prediction
        current_sequence = np.append(current_sequence[:, 1:, :], [next_prediction_scaled], axis=1)

    # Inverse transform the predictions
    predictions = scaler.inverse_transform(predictions_scaled)
    
    # Format the output
    import json
    output = [[int(round(num)) for num in pred] for pred in predictions]
    print(json.dumps(output))

if __name__ == '__main__':
    predict_next_draws()