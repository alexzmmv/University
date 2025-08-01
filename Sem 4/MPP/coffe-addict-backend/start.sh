#!/bin/bash

# Wait for services to be ready if needed
echo "Starting Coffee Addict Backend..."

# Navigate to the app directory
cd /app

# Run the FastAPI application with Uvicorn
exec python -m uvicorn app.server:app --host 0.0.0.0 --port 8000