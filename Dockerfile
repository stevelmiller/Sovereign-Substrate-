FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY CONTRACT.md PHYSICS.md ./

# Expose Flask port
EXPOSE 5000

# Run with gunicorn (1 worker for demo)
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "main:app"]
