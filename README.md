# Mark Six Lottery Prediction

This project is a web application that fetches historical Mark Six lottery data, stores it in a local SQLite database, and uses a machine learning model to predict future lottery numbers.

## Features

-   **Data Fetching:** Fetches historical lottery data from an external API.
-   **Database Storage:** Saves the fetched data into a local SQLite database (`marksix.db`).
-   **Data Export:** Allows exporting the data to a CSV file.
-   **Machine Learning Model:**
    -   Trains an LSTM (Long Short-Term Memory) neural network model using TensorFlow/Keras.
    -   The model is trained on the historical data to learn patterns.
    -   The trained model (`marksix_model.h5`) is saved locally.
-   **Prediction:**
    -   Predicts the next 10 sets of lottery numbers based on the last 10 draws.
    -   Displays the predictions on the web interface.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Python dependencies:**

    Make sure you have Python and pip installed. Then, run the following command to install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Train the Model:**

    Before you can make predictions, you need to train the model. Run the training script:

    ```bash
    python train_model.py
    ```

    This will create the `marksix_model.h5` and `scaler_params.npy` files.

## Usage

1.  **Start the Web Server:**

    Run the proxy server to start the application:

    ```bash
    python proxy.py
    ```

    The server will be running at `http://localhost:8002`.

2.  **Open the Application:**

    Open your web browser and navigate to `http://localhost:8002`.

3.  **Use the Application:**
    -   The application will automatically fetch and display the latest lottery results.
    -   Click **Save to DB** to store the results in the database.
    -   Click **Predict Next Draw** to see the model's predictions for the next 10 draws.

## Changelog

### [Date of last change]

-   **Feature:** Implemented a feature to predict the next 10 sets of lottery numbers.
-   **Model:** Updated the prediction script (`predict.py`) to generate 10 sequential predictions.
-   **Backend:** Modified the proxy server (`proxy.py`) to handle the new prediction format.
-   **Frontend:** Updated the user interface (`index.html` and `script.js`) to display the 10 predictions in a table.

### [Previous Date]

-   **Feature:** Created the initial prediction model.
-   **Model:** Built and trained an LSTM model (`train_model.py`) to predict a single set of numbers.
-   **Backend:** Added a `/predict` endpoint to the proxy server.
-   **Frontend:** Added a "Predict Next Draw" button to the UI.