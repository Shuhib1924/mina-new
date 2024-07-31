import time
import os
import sys

while True:
    try:
        # Your main script logic here
        print("Running script...")
        time.sleep(5)  # Simulating work by sleeping for 5 seconds

    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally log the error or perform cleanup here

    # Reload the script
    print("Reloading script...")
    os.execv(sys.executable, ["python"] + sys.argv)
