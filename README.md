# Mark Six Lottery Prediction

This project is a web application that fetches historical Mark Six lottery data, stores it in a local SQLite database, and uses a machine learning model to predict future lottery numbers.

This project leverages artificial intelligence to generate code, including the machine learning model, prediction logic, and web user interface. The AI also helped establish the folder structure and create installation scripts for Python, TensorFlow, and CUDA on Windows Subsystem for Linux (WSL). Approximately 99% of the implementation was completed through AI assistance, with minimal human intervention (around 1%).

This README was generated with the assistance of AI to ensure comprehensive documentation of the project's features, setup instructions, and usage guidelines. The AI helped structure the content in a clear and organized manner while maintaining technical accuracy.

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

* **Data Fetching:** Fetches historical lottery data from an external API.

* **Database Storage:** Saves the fetched data into a local SQLite database (`data/marksix.db`).

* **Data Export:** Allows exporting the data to a CSV file.

* **History:**

  * Automatically loads and displays all historical lottery data from `marksix.db` on page load.

  * Table headers are sticky for improved usability when scrolling.

  * Features a clean, responsive table layout with a black background and blue headers.

* **Machine Learning Model:**

  * Trains an LSTM (Long Short-Term Memory) neural network model using TensorFlow/Keras.

  * The model is trained on the historical data to learn patterns.

  * The trained model (`data/marksix_model.keras`) is saved locally.

* **Prediction:**

  * Predicts 10 unique sets of 6 lottery numbers.

  * Displays the predictions in a list format.

  * Allows copying the predicted numbers to the clipboard.

## For WSL For GPU

1. **NVIDIA Driver for WSL:**

   Install the latest NVIDIA driver for WSL from the [NVIDIA website](https://developer.nvidia.com/cuda-downloads?target_os=Linux\&target_arch=x86_64\&Distribution=WSL-Ubuntu\&target_version=2.0\&target_type=deb_local).

2. **CUDA on WSL:**

   Follow the official [NVIDIA CUDA on WSL guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) to install the CUDA toolkit.

   The key commands are:

   ```bash
   wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
   sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
   wget https://developer.download.nvidia.com/compute/cuda/12.5.1/local_installers/cuda-repo-wsl-ubuntu-12-5-local_12.5.1-1_amd64.deb
   sudo dpkg -i cuda-repo-wsl-ubuntu-12-5-local_12.5.1-1_amd64.deb
   sudo cp /var/cuda-repo-wsl-ubuntu-12-5-local/cuda-*-keyring.gpg /usr/share/keyrings/
   sudo apt-get update
   sudo apt-get -y install cuda-toolkit-12-5
   ```

3. **Conda Environment Setup:**

   Create and configure a Conda environment for this project:

   ```bash
   conda create --name marksix python=3.12
   conda activate marksix
   pip install -r requirements.txt
      
   ```

   Trouble shooting for tensorflow gpu on wsl

   ```bash
   pip install tensorflow[and-cuda]==2.16.1
   for dir in "$CONDA_PREFIX"/lib/python3.12/site-packages/nvidia/*; do [ -d "$dir/lib" ] && LD_LIBRARY_PATH="$dir/lib:$LD_LIBRARY_PATH"; done
   conda env config vars set LD_LIBRARY_PATH=$LD_LIBRARY_PATH

   conda deactivate
   conda activate marksix

   python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
   //[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
   ```

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DouglasHSK/MarkSix.git
   cd MarkSix
   ```

2. **Install Python dependencies:**

   Make sure you have Python and pip installed. Then, run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Model:**

   Before you can make predictions, you need to train the model. Run the training script:

   ```bash
   python api/train_model.py
   ```

   This will create the `data/marksix_model.keras` and `data/scaler_params.npy` files.

## Usage

### Scripts

This project includes scripts to simplify common tasks on both Windows and Linux.

**Windows**

* **Start the server:**

  ```bash
  start-server.bat
  ```

* **Train the model:**

  ```bash
  train-model.bat [epochs] [device]
  ```

  * `epochs` (optional): The number of training epochs (default: 2000).

  * `device` (optional): The training device, either `gpu` or `cpu` (default: `gpu`).

  **Example:**

  ```bash
  train-model.bat 5000 cpu
  ```

* **Run prediction:**

  ```bash
  predict.bat
  ```

**Linux**

* **Start the server:**

  ```bash
  chmod +x start-server.sh
  ./start-server.sh
  ```

* **Train the model:**

  ```bash
  chmod +x train-model.sh
  ./train-model.sh [epochs] [device]
  ```

  * `epochs` (optional): The number of training epochs (default: 2000).

  * `device` (optional): The training device, either `gpu` or `cpu` (default: `gpu`).

  **Example:**

  ```bash
  ./train-model.sh 5000 cpu
  ```

* **Run prediction:**

  ```bash
  chmod +x predict.sh
  ./predict.sh
  ```

### Manual Usage

1. **Start the Web Server:**

   Run the proxy server to start the application:

   ```bash
   python api/proxy.py
   ```

   The server will be running at `http://localhost:8002`.

2. **Open the Application:**

   Open your web browser and navigate to `http://localhost:8002`.

3. **Use the Application:**

   * The application will automatically fetch and display the latest lottery results.

   * Click **Save to DB** to store the results in the database.

   * Click **Predict Next Draw** to see the model's predictions for the next 10 draws.

## Docker Support

This project includes a `Dockerfile` to build a containerized version of the application.

### Build the Docker Image

To build the Docker image, run the following command from the project's root directory:

```bash
docker build -t marksix-app -f docker/Dockerfile .
```

### Run the Docker Container

Once the image is built, you can run the application in a Docker container:

```bash
docker run -d -p 8002:8002 --name marksix-container marksix-app
```

The application will be accessible at `http://localhost:8002`.

## Changelog

### 2025-08-16 (History Feature)

* **Feature:** Added a history view to display all lottery records from the database.

* **Enhancement:** Implemented sticky table headers for better scrolling.

* **Style:** Updated the history view with a new visual design.

### 2025-07-28 (Docker Support)

* **Docker:** Added a `Dockerfile` to containerize the application.

* **Docs:** Updated the `README.md` with instructions for building and running the Docker container.

### 2025-07-27 (WSL GPU Setup)

* **WSL:** Configured the WSL environment for GPU-accelerated model training.

* **CUDA:** Installed the NVIDIA CUDA Toolkit and cuDNN.

* **Docs:** Updated the `README.md` with detailed instructions for setting up the WSL environment.

### 2025-07-26 (Refactor)

* **Refactor:** Restructured the project into `api`, `data`, and `public` directories for better organization.

* **Refactor:** Updated all file paths to reflect the new directory structure.

* **Model:** Changed the model saving format from `.h5` to the recommended `.keras` format.

### 2025-07-26

* **Enhancement:** Updated the progress indicator to be a larger, more visually appealing dialog with a blurred background.

* **Enhancement:** Changed the prediction results display from a grid to a list for better readability.

* **Feature:** Added a "Copy to Clipboard" button for the predicted numbers.

* **Fix:** Resolved a `TypeError` in `predict.py` related to JSON serialization of NumPy integer types.

* **Style:** Updated `style.css` to format the new list, button, and progress dialog.

### 2025-07-25

* **Feature:** Implemented a feature to predict the next 10 sets of lottery numbers.

* **Model:** Updated the prediction script (`predict.py`) to generate 10 sequential predictions.

* **Backend:** Modified the proxy server (`proxy.py`) to handle the new prediction format.

* **Frontend:** Updated the user interface (`index.html` and `script.js`) to display the 10 predictions in a table.

### 2025-07-24

* **Feature:** Created the initial prediction model.

* **Model:** Built and trained an LSTM model (`train_model.py`) to predict a single set of numbers.

* **Backend:** Added a `/predict` endpoint to the proxy server.

* **Frontend:** Added a "Predict Next Draw" button to the UI.

