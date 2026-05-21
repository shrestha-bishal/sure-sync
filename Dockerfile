# Stage 1: Base (dependencies and shared)
FROM python:3.12-slim AS base

# Set workdir
WORKDIR /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app

# Stage 2: worker
FROM base AS worker-stage
COPY app/ .

# Run the app
CMD ["python", "-u", "main.py"]

# Stage 3: web
FROM base AS web-stage
COPY web/ .

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" ]