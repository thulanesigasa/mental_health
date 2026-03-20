# Use an official standard Python image
FROM python:3.10-slim

# Set strict environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py

# Set root work directory
WORKDIR /app

# Install system dependencies req'd for psycopg2 & argon2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies efficiently
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy platform architecture
COPY . /app/

# Expose standardized Web Port
EXPOSE 8000

# Execute Gunicorn in production config
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "run:app"]
