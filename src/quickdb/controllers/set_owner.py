import subprocess
from quickdb.utils.constants import production

def set_owner(canister_name: str, principal: str):
    """Set the owner for a specific canister."""
    print(f"Testing canister functions for {canister_name}...")
    try:
        result = subprocess.run(
            ["dfx", "canister", "call", canister_name, "setOwner", principal],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )

        if result.returncode != 0:
            print("Error testing canister.")
            print(result.stderr)
        else:
            print("Test completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
