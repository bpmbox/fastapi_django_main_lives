#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create a SQLite database
export DATABASE_URL=sqlite:///./sql_app.db
python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); Base.metadata.create_all(engine)"

# Run the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000
