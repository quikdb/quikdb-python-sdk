import subprocess
import shutil
from quickdb.utils.constants import production

def deploy_to_local(principal_id: str):
    """Deploy the database to a local canister using dfx."""
    if not shutil.which("dfx"):
        print("quikdb is not installed. Please run `quikdb install` first.")
        return

    print("Requesting permissions to create virtual database...")
    create_canister_result = subprocess.run(
        ["dfx", "canister", "create", "database"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if create_canister_result.returncode != 0:
        print("Error starting code.", create_canister_result.stderr)
        return

    print("Requesting permissions to run local tests...")
    create_test_canister_result = subprocess.run(
        ["dfx", "canister", "create", "test"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if create_test_canister_result.returncode != 0:
        print("Error starting code.", create_test_canister_result.stderr)
        return

    print("Requesting permissions to build variations...")
    build_result = subprocess.run(
        ["dfx", "build"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if build_result.returncode != 0:
        print("Error building code.", build_result.stderr)
        return

    print("Requesting permissions to set up your database...")
    subprocess.run(
        ["dfx", "ledger", "fabricate-cycles", "--t", "1000000", "--canister", "database"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    subprocess.run(
        ["dfx", "ledger", "fabricate-cycles", "--t", "1000000", "--canister", "test"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("Requesting permissions to deposit testnets...")
    subprocess.run(
        ["dfx", "canister", "deposit-cycles", "--all", "10T"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("Requesting permissions to deploy to testnet...")
    deploy_result = subprocess.run(
        ["dfx", "deploy"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if deploy_result.returncode != 0:
        print("Error deploying to local canister.", deploy_result.stderr)
    else:
        print("Code deployed to local canister successfully.")
        backend_url_match = None
        for line in deploy_result.stderr.splitlines():
            if "database:" in line and "http://" in line:
                backend_url_match = line.split("http://", 1)[-1].strip()

        if backend_url_match:
            print("Requesting permissions to generate codes...")
            generate_result = subprocess.run(
                ["dfx", "generate", "database"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if generate_result.returncode != 0:
                print("Error generating declarations file", generate_result.stderr)
                return

            return f"http://{backend_url_match}"
        else:
            print("Backend URL not found.")
