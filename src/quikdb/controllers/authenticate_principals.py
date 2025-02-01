import os
import subprocess
import time
import shutil
from quikdb.utils.constants import production

def authenticate_principal(username: str, principal_id: str):
    """Authenticate a principal using dfx."""
    if not shutil.which("dfx"):
        print("dfx is not installed. Please run `quikdb install-dfx` first.")
        return False

    print(f"Authenticating principal: {username}")

    # Step 1: Ensure dfx is running
    print("Reaching out to server...")
    try:
        # Stop any running dfx instance
        stop_result = subprocess.run(
            ["dfx", "stop"],
            stdout=None,
            stderr=None,
            text=True,
            check=False
        )
        if stop_result.returncode != 0:
            print(f"Warning: Unable to stop dfx. Continuing... {stop_result.stderr}")

        # Start dfx in the background
        start_result = subprocess.run(
            ["nohup", "dfx", "start", "--clean", "--background"],
            stdout=None,
            stderr=None,
            text=True,
            check=False
        )
        if start_result.returncode != 0:
            print("Error starting dfx.", start_result.stderr)
            return False

    except Exception as e:
        print(f"Error starting dfx: {e}")
        return False

    # Wait for dfx to initialize
    time.sleep(5)

    # Step 2: Set and authorize controller
    print("Setting controller...")
    try:
        set_controller_result = subprocess.run(
            ["dfx", "wallet", "add-controller", principal_id],
            stdout=None,
            stderr=None,
            text=True,
            check=False
        )
        if set_controller_result.returncode != 0:
            print("Error setting controller.", set_controller_result.stderr)
            return False

        print("Authorizing principal...")
        authorize_controller_result = subprocess.run(
            ["dfx", "wallet", "authorize", principal_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        if authorize_controller_result.returncode != 0:
            print("Error authorizing controller.", authorize_controller_result.stderr)
            return False

        print(f"Authenticated as principal: {username}")
        return True

    except Exception as e:
        print(f"Error setting or authorizing controller: {e}")
        return False
