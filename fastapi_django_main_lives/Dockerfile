# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gradio==4.29.0 && \
    pip install --no-cache-dir google-cloud-storage google-auth google-auth-oauthlib google-auth-httplib2 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create directories for gradio cache and temp files
RUN mkdir -p /app/gradio_cached_examples && \
    mkdir -p /app/cache && \
    chmod -R 755 /app

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Run the application
CMD ["python", "app.py"]