#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run API
python api/app.py &

# Run frontend
python frontend/app.py
