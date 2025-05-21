from celery_config import app # Import the Celery app instance
import time
import random
import os

CONTAINER_INPUT_DIR = "/app/worker_input_files/"

# Define a custom exception for validation errors
class TaskValidationError(Exception):
    pass

@app.task(bind=True, name='tasks.run_simulation_and_upload')
def run_simulation_and_upload(self, job_params):
    job_id = self.request.id
    print(f"WORKER (Docker) [{job_id}]: Received job with params: {job_params}")
    os.makedirs(CONTAINER_INPUT_DIR, exist_ok=True) # Ensure dir exists

    self.update_state(state='VALIDATING', meta={'status': 'Checking input files...'})
    print(f"WORKER (Docker) [{job_id}]: Validating inputs...")
    time.sleep(0.5)

    input_file_name = job_params.get('input_file_name')
    if not input_file_name:
        print(f"WORKER (Docker) [{job_id}]: VALIDATION FAILED - 'input_file_name' parameter missing.")
        # Raise your custom exception
        raise TaskValidationError("'input_file_name' parameter missing.")

    simulated_file_path = os.path.join(CONTAINER_INPUT_DIR, input_file_name)
    if not os.path.exists(simulated_file_path):
        print(f"WORKER (Docker) [{job_id}]: VALIDATION FAILED - Input file '{simulated_file_path}' not found IN CONTAINER.")
        # Raise your custom exception
        raise TaskValidationError(f"Input file '{input_file_name}' not found by worker in container.")

    print(f"WORKER (Docker) [{job_id}]: Inputs validated successfully for '{input_file_name}'.")

    self.update_state(state='PROCESSING', meta={'status': 'Running computation...'})
    print(f"WORKER (Docker) [{job_id}]: Starting computation...")
    computation_duration = job_params.get('duration', random.randint(2, 4))
    for i in range(computation_duration):
        progress = ((i + 1) / computation_duration) * 100
        self.update_state(state='PROCESSING', meta={'status': f'Processing... {i+1}/{computation_duration}', 'progress': f'{progress:.2f}%'})
        print(f"WORKER (Docker) [{job_id}]: Computing... step {i+1}/{computation_duration}")
        time.sleep(1)
    print(f"WORKER (Docker) [{job_id}]: Computation finished.")

    self.update_state(state='UPLOADING', meta={'status': 'Uploading results...'})
    print(f"WORKER (Docker) [{job_id}]: Simulating result upload...")
    time.sleep(0.5)
    gcs_folder_name = job_id
    gcs_url = f"gs://your-results-bucket/{gcs_folder_name}/output_data.dat"
    print(f"WORKER (Docker) [{job_id}]: Results would be at {gcs_url}")

    return {'status': 'SUCCESS', 'job_id': job_id, 'gcs_url': gcs_url}