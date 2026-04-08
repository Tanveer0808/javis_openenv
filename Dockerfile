# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Environment variable for python path
ENV PYTHONPATH=/app

# Default command runs the Flask App
CMD ["python", "app.py"]
