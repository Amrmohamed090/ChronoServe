# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY app ./app

# Set PYTHONPATH so 'app' is importable
ENV PYTHONPATH=/app

# Expose FastAPI port
EXPOSE 8080

# Run FastAPI using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
