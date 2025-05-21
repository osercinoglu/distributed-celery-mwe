FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY celery_config.py .
COPY tasks.py .
# If tasks.py imports other local modules, copy them too

# Create the directory for dummy input files and copy one in for the "valid" task scenario
RUN mkdir -p /app/worker_input_files/
COPY worker_input_files/simulation_config_001.txt /app/worker_input_files/simulation_config_001.txt

# Modified CMD to print env vars before starting Celery worker
CMD ["sh", "-c", "echo '---- ENV VARS INSIDE CONTAINER ----' && \
                  echo 'CELERY_BROKER_HOST: ' $CELERY_BROKER_HOST && \
                  echo 'CELERY_BROKER_PORT: ' $CELERY_BROKER_PORT && \
                  echo 'CELERY_BROKER_USER: ' $CELERY_BROKER_USER && \
                  echo 'CELERY_BROKER_PASSWORD: ' $CELERY_BROKER_PASSWORD && \
                  echo 'CELERY_RESULT_BACKEND_HOST: ' $CELERY_RESULT_BACKEND_HOST && \
                  echo 'CELERY_RESULT_BACKEND_PORT: ' $CELERY_RESULT_BACKEND_PORT && \
                  echo '-----------------------------------' && \
                  celery -A celery_config.app worker --loglevel=INFO -P solo"]