# Use slim Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system deps (optional: for debugging, clean apt cache)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl tini && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY app ./app

# Use tini for signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
