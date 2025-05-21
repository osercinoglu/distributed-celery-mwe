from tasks import run_simulation_and_upload # Imports the task function from tasks.py
import os
import time

# This script runs on the DO droplet. It doesn't interact with files on the worker.
# The 'input_file_name' it sends is what the worker task expects to find *inside its container*.

if __name__ == "__main__":
    print("PRODUCER: Preparing to send tasks...")

    # Task 1: Valid input (worker's Docker image should have this file)
    valid_input_params = {
        'input_file_name': "simulation_config_001.txt", # This file needs to be in the Docker image
        'simulation_type': 'MWE_valid',
        'user_id': 'user123',
        'duration': 3 # Override random duration for predictability
    }
    task_valid = run_simulation_and_upload.delay(valid_input_params)
    print(f"PRODUCER: Sent VALID task. Job ID: {task_valid.id}")
    time.sleep(0.1) # Slight delay between sends

    # Task 2: Input file missing inside worker's Docker image
    missing_file_params = {
        'input_file_name': "non_existent_file_in_container.txt",
        'user_id': 'user456',
        'duration': 1
    }
    task_missing = run_simulation_and_upload.delay(missing_file_params)
    print(f"PRODUCER: Sent MISSING FILE task. Job ID: {task_missing.id}")
    time.sleep(0.1)

    # Task 3: Input parameter missing (input_file_name)
    missing_param_params = {
        # 'input_file_name' is deliberately missing
        'user_id': 'user789',
        'duration': 1
    }
    task_no_param = run_simulation_and_upload.delay(missing_param_params)
    print(f"PRODUCER: Sent MISSING PARAM task. Job ID: {task_no_param.id}")

    print("\nPRODUCER: All tasks sent. You can now check their status with check_status.py")
    print(f"Example (after worker processes): python3 check_status.py {task_valid.id}")