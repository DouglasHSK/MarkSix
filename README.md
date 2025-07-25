# Mark Six Lottery Prediction

This project is a web application that fetches historical Mark Six lottery data, stores it in a local SQLite database, and uses a machine learning model to predict future lottery numbers.

## Project Structure

```
.
├── api
│   ├── predict.py         # Handles predictions
│   ├── proxy.py           # The web server
│   └── train_model.py     # The model training script
├── data
│   ├── marksix.db         # The SQLite database
│   ├── marksix_model.keras  # The trained model
│   └── scaler_params.npy  # The scaler parameters
├── public
│   ├── index.html         # The main HTML file
│   ├── script.js          # The main JavaScript file
│   └── style.css          # The main CSS file
└── requirements.txt
```

## Features

-   **Data Fetching:** Fetches historical lottery data from an external API.
-   **Database Storage:** Saves the fetched data into a local SQLite database (`data/marksix.db`).
-   **Data Export:** Allows exporting the data to a CSV file.
-   **Machine Learning Model:**
    -   Trains an LSTM (Long Short-Term Memory) neural network model using TensorFlow/Keras.
    -   The model is trained on the historical data to learn patterns.
    -   The trained model (`data/marksix_model.keras`) is saved locally.
-   **Prediction:**
    -   Predicts 10 unique sets of 6 lottery numbers.
    -   Displays the predictions in a list format.
    -   Allows copying the predicted numbers to the clipboard.

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
    python api/train_model.py
    ```

    This will create the `data/marksix_model.keras` and `data/scaler_params.npy` files.

## Usage

### Scripts

This project includes scripts to simplify common tasks on both Windows and Linux.

**Windows**

-   **Start the server:**
    ```bash
    start-server.bat
    ```
-   **Train the model:**
    ```bash
    train-model.bat
    ```
-   **Run prediction:**
    ```bash
    predict.bat
    ```

**Linux**

-   **Start the server:**
    ```bash
    chmod +x start-server.sh
    ./start-server.sh
    ```
-   **Train the model:**
    ```bash
    chmod +x train-model.sh
    ./train-model.sh
    ```
-   **Run prediction:**
    ```bash
    chmod +x predict.sh
    ./predict.sh
    ```

### Manual Usage

1.  **Start the Web Server:**

    Run the proxy server to start the application:

    ```bash
    python api/proxy.py
    ```

    The server will be running at `http://localhost:8002`.

2.  **Open the Application:**

    Open your web browser and navigate to `http://localhost:8002`.

3.  **Use the Application:**
    -   The application will automatically fetch and display the latest lottery results.
    -   Click **Save to DB** to store the results in the database.
    -   Click **Predict Next Draw** to see the model's predictions for the next 10 draws.

## Changelog

### 2025-07-26 (Refactor)

-   **Refactor:** Restructured the project into `api`, `data`, and `public` directories for better organization.
-   **Refactor:** Updated all file paths to reflect the new directory structure.
-   **Model:** Changed the model saving format from `.h5` to the recommended `.keras` format.

### 2025-07-26

-   **Enhancement:** Updated the progress indicator to be a larger, more visually appealing dialog with a blurred background.
-   **Enhancement:** Changed the prediction results display from a grid to a list for better readability.
-   **Feature:** Added a "Copy to Clipboard" button for the predicted numbers.
-   **Fix:** Resolved a `TypeError` in `predict.py` related to JSON serialization of NumPy integer types.
-   **Style:** Updated `style.css` to format the new list, button, and progress dialog.

### 2025-07-25

-   **Feature:** Implemented a feature to predict the next 10 sets of lottery numbers.
-   **Model:** Updated the prediction script (`predict.py`) to generate 10 sequential predictions.
-   **Backend:** Modified the proxy server (`proxy.py`) to handle the new prediction format.
-   **Frontend:** Updated the user interface (`index.html` and `script.js`) to display the 10 predictions in a table.

### 2025-07-24

-   **Feature:** Created the initial prediction model.
-   **Model:** Built and trained an LSTM model (`train_model.py`) to predict a single set of numbers.
-   **Backend:** Added a `/predict` endpoint to the proxy server.
-   **Frontend:** Added a "Predict Next Draw" button to the UI.