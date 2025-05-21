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

# Command to run the Celery worker
# It will pick up broker/backend URLs from environment variables
CMD ["celery", "-A", "celery_config.app", "worker", "--loglevel=INFO", "-P", "solo"]