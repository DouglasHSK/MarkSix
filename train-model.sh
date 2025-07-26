#!/bin/bash
echo "Training the model..."
EPOCHS=${1:-2000}
DEVICE=${2:-gpu}

python3 api/train_model.py --epochs $EPOCHS --device $DEVICE