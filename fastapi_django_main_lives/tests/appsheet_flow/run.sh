#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover -v tests

# Run main script
python main.py
