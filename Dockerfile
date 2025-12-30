# Use official Python image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy files
COPY app/ ./app/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "-u", "app/main.py"]