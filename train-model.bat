@echo off
echo Training the model...
set EPOCHS=%1
set DEVICE=%2

if not defined EPOCHS set EPOCHS=2000
if not defined DEVICE set DEVICE=gpu

python api/train_model.py --epochs %EPOCHS% --device %DEVICE%