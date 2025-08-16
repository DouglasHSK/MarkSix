import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import sqlite3
import json
import sys

# Function to load the last sequence of data
def load_last_sequence():
    conn = sqlite3.connect('data/marksix.db')
    cursor = conn.cursor()
    cursor.execute("SELECT no1, no2, no3, no4, no5, no6 FROM results ORDER BY draw_date DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return np.array(rows)

# Main function to make a prediction
def predict_next_draws(num_predictions=10):
    try:
        # Check for available GPUs
        gpu=0
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            print(f"GPUs found: {len(gpus)}")
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        else:
            print("No GPUs found. Training on CPU.")


        # Load the trained model and scaler C:\Users\user\Documents\Test\Web\data\marksix_model.keras
        model = tf.keras.models.load_model('data/marksix_model.keras', compile=False)
        
        scaler_params = np.load('data/scaler_params.npy', allow_pickle=True).item()
        scaler = MinMaxScaler()
        scaler.min_ = scaler_params['min']
        scaler.scale_ = scaler_params['scale']

        # Load the last sequence of data
        last_sequence = load_last_sequence()
        last_sequence_scaled = scaler.transform(last_sequence)

        candidate_predictions_scaled = []
        current_sequence = last_sequence_scaled.reshape((1, 10, 6))

        # Generate more candidates to ensure we can find enough unique sets
        num_candidates = 50
        for _ in range(num_candidates):
            # Make a prediction
            next_prediction_scaled = model.predict(current_sequence, verbose=0)
            candidate_predictions_scaled.append(next_prediction_scaled[0])
            
            # Update the sequence for the next prediction
            current_sequence = np.append(current_sequence[:, 1:, :], [next_prediction_scaled], axis=1)

        # Inverse transform the predictions
        candidate_predictions = scaler.inverse_transform(candidate_predictions_scaled)
    
        unique_predictions = []
        seen_sets = set()

        for pred in candidate_predictions:
            # Round, clip to be within 1-49 range, and convert to int
            numbers = np.clip(np.round(pred), 1, 49).astype(int)
            
            # Check for internal duplicates
            if len(set(numbers)) == 6:
                # Sort to have a canonical representation for checking set uniqueness
                sorted_numbers = tuple(sorted(numbers))
                
                # Check if this set of numbers has been seen before
                if sorted_numbers not in seen_sets:
                    seen_sets.add(sorted_numbers)
                    unique_predictions.append([int(n) for n in sorted_numbers])
                    
                    # Stop when we have enough unique predictions
                    if len(unique_predictions) == num_predictions:
                        break
        
        # Convert to JSON and print
        print(json.dumps({
            'predictions': unique_predictions[:num_predictions]
        }))
    except Exception as e:
        print(json.dumps({
            'error': str(e)
        }))
        sys.exit(1)

if __name__ == '__main__':
    predict_next_draws()