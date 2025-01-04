import subprocess
from quickdb.utils.constants import production

def deploy_to_production(canister_name: str):
    """Deploy a canister to the IC network."""
    print(f"Deploying {canister_name} to the IC network...")

    try:
        # Build the project
        build_result = subprocess.run(
            ["dfx", "build"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )

        if build_result.returncode != 0:
            print("Error building code.")
            return

        # Deploy to the IC network
        canister_id_result = subprocess.run(
            ["dfx", "deploy", "--network", "ic"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )

        if canister_id_result.returncode != 0:
            print("Error retrieving canister ID.")
            return

        # Extract and log the canister ID
        canister_id = canister_id_result.stdout.strip()
        print(f"Canister created with ID: {canister_id}")

    except Exception as e:
        print(f"An error occurred during deployment: {e}")
