# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create staticfiles directory
RUN mkdir -p /app/static

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8090

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8090", "--workers", "4", "inventory.wsgi:application"]
