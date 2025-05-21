from celery_config import app # Import the Celery app instance
from celery.result import AsyncResult
import sys
import time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_status.py <task_id_1> [<task_id_2> ...]")
        sys.exit(1)

    task_ids = sys.argv[1:]

    for task_id in task_ids:
        print(f"\n--- Checking status for Task ID: {task_id} ---")
        # Create an AsyncResult instance to query the backend
        result_obj = AsyncResult(task_id, app=app)

        print(f"Current Status: {result_obj.status}")

        if result_obj.ready(): # True if the task has finished (either success or failure)
            if result_obj.successful():
                print("Task Succeeded!")
                print(f"Result Type: {type(result_obj.result)}")
                print(f"Result Value: {result_obj.result}")
            elif result_obj.failed():
                print("Task Failed!")
                print(f"Exception: {result_obj.result}") # The exception instance
                print(f"Traceback:\n{result_obj.traceback}")
            else:
                # Other terminal states like REVOKED
                print(f"Task finished with unhandled state: {result_obj.status}")
        else: # Task is still pending or in a custom state like PROGRESS
            print("Task is not yet ready (still PENDING or PROCESSING).")
            if result_obj.info: # Holds metadata from update_state()
                 print(f"Current Meta-Info/Progress: {result_obj.info}")
    print("\n--- Status check complete ---")