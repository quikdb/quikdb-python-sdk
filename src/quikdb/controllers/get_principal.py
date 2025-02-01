import shutil
import subprocess
from quikdb.controllers.create_principals import create_principal
from quikdb.utils.constants import production

def get_principal(username: str):
    """Retrieve the principal ID for the specified username."""
    if not shutil.which("dfx"):
        print("dfx is not installed. Please run `quikdb install-dfx` first.")
        return {"status": False}

    try:
        # Try to get the principal ID
        principal_id_result = subprocess.run(
            ["dfx", "identity", "get-principal", "--identity", username],
            stdout=subprocess.PIPE,
            stderr=None,
            text=True,
            check=False
        )

        seed_phrase = ""

        if principal_id_result.returncode != 0:
            print("Error retrieving principal ID.")
            print("Creating principal...")
            create_principal_response = create_principal(username)
            print('the principal response', create_principal_response)
            

            if not create_principal_response["status"]:
                print("Installation failed.")
                return {"status": False}

            # Retry getting the principal ID
            principal_id_result = subprocess.run(
                ["dfx", "identity", "get-principal", "--identity", username],
                stdout=subprocess.PIPE,
                stderr=None,
                text=True,
                check=False
            )
            seed_phrase = create_principal_response.get("seedPhrase", "")

        principal_id = principal_id_result.stdout.strip()
        print(f"Current Principal ID: {principal_id}")

        return {"status": True, "data": {"principalId": principal_id, "seedPhrase": seed_phrase}}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": False}
