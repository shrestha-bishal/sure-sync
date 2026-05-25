# Stage 1: Base (dependencies and shared)
FROM python:3.12-slim AS base

# Set workdir
WORKDIR /app
COPY requirements.txt .
COPY core/ ./core/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app

# Stage 2: worker
FROM base AS worker-stage
COPY worker/ ./worker/

# Run the app
CMD ["python", "-u", "worker/main.py"]

# Stage 3: web
FROM base AS web-stage
COPY worker/models ./worker/models
COPY worker/helpers ./worker/helpers
COPY web/ ./web/

CMD [ "uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000" ]