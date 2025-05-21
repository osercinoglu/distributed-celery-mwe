from celery import Celery
import os

# --- Connection Settings ---
# These will be set by environment variables depending on where the code runs.
RABBITMQ_HOST = os.environ.get('CELERY_BROKER_HOST', 'localhost')
RABBITMQ_PORT = os.environ.get('CELERY_BROKER_PORT', '5672') # Standard RabbitMQ port
RABBITMQ_USER = os.environ.get('CELERY_BROKER_USER', 'guest')
RABBITMQ_PASS = os.environ.get('CELERY_BROKER_PASSWORD', 'guest')

REDIS_HOST = os.environ.get('CELERY_RESULT_BACKEND_HOST', 'localhost')
REDIS_PORT = os.environ.get('CELERY_RESULT_BACKEND_PORT', '6379') # Standard Redis port
# REDIS_PASSWORD = os.environ.get('CELERY_REDIS_PASSWORD', None) # If Redis is password protected

RABBITMQ_BROKER_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//'
# If Redis has a password: f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
REDIS_BACKEND_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'


# --- Celery App Definition ---
app = Celery('my_celery_project_tasks', # A name for your Celery app
             broker=RABBITMQ_BROKER_URL,
             backend=REDIS_BACKEND_URL,
             include=['tasks']) # Assumes tasks.py is discoverable

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

if __name__ == '__main__':
    app.start() # Not typically run this way, but good for `celery -A celery_config ...`