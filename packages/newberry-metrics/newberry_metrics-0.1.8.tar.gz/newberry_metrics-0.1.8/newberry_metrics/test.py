from main import TokenEstimator, SessionMetrics, APICallMetrics
from datetime import datetime, timedelta
import os
import time
import requests
import json
import sys


# --- Test Script ---
if __name__ == "__main__":
    # --- Configuration ---
    test_model_id = "anthropic.claude-3-haiku-20240307-v1:0" # Use a cheap/fast model
    fetch_timeout = 5 # Seconds to wait for HTTP response
    pause_between_steps = 1.5 # Seconds to wait after API call before fetching URL

    # --- Import the class ---
    try:
        # Assuming the package is installed
        from main import TokenEstimator
    except ImportError:
        print("ERROR: Cannot import TokenEstimator.")
        print("Make sure the 'newberry_metrics' package is installed ('pip install .')")
        print("or adjust the Python path.")
        sys.exit(1)

    # --- Check for requests library ---
    try:
        import requests
    except ImportError:
        print("ERROR: 'requests' library not found.")
        print("Please install it: pip install requests")
        sys.exit(1)


    print("--- Testing Web Viewer Update ---")
    estimator = None
    metrics_url = None
    initial_total_calls = -1
    updated_total_calls = -1

    try:
        # 1. Initialize TokenEstimator (starts web server)
        print(f"Initializing TokenEstimator with model: {test_model_id}...")
        estimator = TokenEstimator(model_id=test_model_id)
        metrics_url = estimator.metrics_url

        if not metrics_url:
            print("ERROR: metrics_url was not set by TokenEstimator.")
            print("Ensure web dependencies are installed ('pip install .[web]') and server started.")
            sys.exit(1)

        print(f"Web viewer URL: {metrics_url}")


        # 3. Make an API Call (triggers JSON update)
        print(f"\nMaking Bedrock API call...")
        prompt = "What are prime numbers?"
        try:
            bedrock_response = estimator._invoke_bedrock(prompt, max_tokens=10)
            print("API call completed.")
            # Optionally check bedrock_response['SessionMetrics'] here if needed
        except Exception as call_e:
            print(f"ERROR during Bedrock API call: {call_e}")
            print("Check AWS credentials and Bedrock model access.")
            # Decide if you want to stop the test entirely on API call failure
            # sys.exit(1)
            print("Attempting to proceed with verification despite API call error...")

        # 4. Wait briefly for file system
        time.sleep(pause_between_steps)

        # 5. Fetch Updated State from URL
        # ... (try/except block for updated fetch) ...

        # 6. Verify Update
        # ... (verification logic) ...

        print("\nTest finished.")

    except ValueError as e:
        # Catches errors specifically during TokenEstimator init (like no credentials)
        print(f"\nERROR during TokenEstimator init: {e}")
        # Indicate test failure
        # sys.exit(1) # Optional: exit if needed

    except ImportError as e:
         # Catches import errors if the package/dependencies aren't right
         print(f"\nIMPORT ERROR: {e}. Ensure package/dependencies are installed.")
         # sys.exit(1) # Optional: exit

    except Exception as e:
        # Catches any other unexpected error during the test sequence
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}", exc_info=True) # Show traceback
        # sys.exit(1) # Optional: exit
