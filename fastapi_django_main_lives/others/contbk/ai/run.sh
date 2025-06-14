#!/bin/bash

# Install dependencies
python -m pip install --user -r requirements.txt

# Run the code
python app/controllers/scraping.py
