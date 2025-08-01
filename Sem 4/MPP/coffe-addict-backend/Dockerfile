FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev \
    ffmpeg \
    curl \
    netcat-openbsd \
    iputils-ping \
    dnsutils \
    iproute2 \
    host \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for video storage
RUN mkdir -p vid/uploads vid/thumbnails vid/temp_chunks

# Instead of using start.sh, we'll run the command directly in the Dockerfile
# This avoids any issues with script execution format

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application directly
CMD ["python", "-m", "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
