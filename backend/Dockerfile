FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
# Explicitly install gunicorn and uvicorn to ensure they are in the PATH
RUN pip install --no-cache-dir gunicorn uvicorn[standard]
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use the full path to gunicorn just to be safe
CMD ["python", "-m", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]