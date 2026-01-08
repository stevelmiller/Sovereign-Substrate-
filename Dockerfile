# Sovereign Substrate (Build 10) - Dockerfile
# Base image: python:3.10-slim as specified
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY CONTRACT.md .
COPY README.md .

# Expose port for the Flask API (if implemented)
EXPOSE 5000

# Run the Lagrangian Substrate
CMD ["python", "main.py"]
