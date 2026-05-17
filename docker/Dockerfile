FROM python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    tor \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies with timeout + retries
RUN pip install --default-timeout=120 --retries=5 --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Run app
CMD ["python", "main.py"]
