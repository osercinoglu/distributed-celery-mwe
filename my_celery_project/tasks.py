from celery_config import app # Import the Celery app instance
import time
import random
import os

# This path will be inside the Docker container for the worker
CONTAINER_INPUT_DIR = "/app/worker_input_files/"

@app.task(bind=True, name='tasks.run_simulation_and_upload')
def run_simulation_and_upload(self, job_params):
    job_id = self.request.id # Get the unique ID for this task
    print(f"WORKER (Docker) [{job_id}]: Received job with params: {job_params}")

    # --- 1. Input Validation Step ---
    self.update_state(state='VALIDATING', meta={'status': 'Checking input files...'})
    print(f"WORKER (Docker) [{job_id}]: Validating inputs...")
    time.sleep(0.5) # Simulate I/O for validation

    input_file_name = job_params.get('input_file_name')
    if not input_file_name:
        print(f"WORKER (Docker) [{job_id}]: VALIDATION FAILED - 'input_file_name' parameter missing.")
        self.update_state(state='FAILURE', meta={'error_type': 'Validation Error', 'reason': "'input_file_name' parameter missing."})
        return {'status': 'FAILURE', 'job_id': job_id, 'error': "'input_file_name' parameter missing."}

    # Worker looks for the file inside its container at this path
    simulated_file_path = os.path.join(CONTAINER_INPUT_DIR, input_file_name)
    if not os.path.exists(simulated_file_path):
        print(f"WORKER (Docker) [{job_id}]: VALIDATION FAILED - Input file '{simulated_file_path}' not found IN CONTAINER.")
        self.update_state(state='FAILURE', meta={'error_type': 'File Not Found', 'reason': f"Input file '{input_file_name}' not found by worker in container."})
        return {'status': 'FAILURE', 'job_id': job_id, 'error': f"Input file '{input_file_name}' not found by worker in container."}

    print(f"WORKER (Docker) [{job_id}]: Inputs validated successfully for '{input_file_name}'.")

    # --- 2. Computation Step ---
    self.update_state(state='PROCESSING', meta={'status': 'Running computation...'})
    print(f"WORKER (Docker) [{job_id}]: Starting computation...")

    computation_duration = job_params.get('duration', random.randint(2, 4)) # Shorter for testing
    for i in range(computation_duration):
        progress = ((i + 1) / computation_duration) * 100
        self.update_state(state='PROCESSING', meta={'status': f'Processing... {i+1}/{computation_duration}', 'progress': f'{progress:.2f}%'})
        print(f"WORKER (Docker) [{job_id}]: Computing... step {i+1}/{computation_duration}")
        time.sleep(1)

    print(f"WORKER (Docker) [{job_id}]: Computation finished.")

    # --- 3. Upload to GCS (Simulated) & Return URL ---
    self.update_state(state='UPLOADING', meta={'status': 'Uploading results...'}) # Placeholder
    print(f"WORKER (Docker) [{job_id}]: Simulating result upload...")
    time.sleep(0.5) # Simulate upload time
    gcs_folder_name = job_id # Use Celery task ID as job_id for folder name
    gcs_url = f"gs://your-results-bucket/{gcs_folder_name}/output_data.dat" # Example URL
    print(f"WORKER (Docker) [{job_id}]: Results would be at {gcs_url}")

    return {'status': 'SUCCESS', 'job_id': job_id, 'gcs_url': gcs_url}