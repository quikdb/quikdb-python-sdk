import os
import shutil
import subprocess
import json
from pathlib import Path
from zipfile import ZipFile
# import readline
from quickdb.utils.toolbox import Tools
from quickdb.controllers import (
    authenticate_principal,
    deploy_to_local,
    get_principal,
    install_dfx
)
from quickdb.http import authenticate_cli, encrypt_user_data, upload_project_code  # Adjust module names as needed

def install_command(args):
    """Checks if QuikDB is installed and installs it if necessary."""
    config_file = Path(Tools.CONFIG_FILE)
    
    if config_file.exists():
        with config_file.open("r") as f:
            config_data = f.read()
        
        print("Current Configuration:")
        config_json = Tools.get_config_as_json(config_data)

        identity = config_json.get("identity")
        username = config_json.get("username")
        project_token_ref = config_json.get("projectTokenRef")

        if not username:
            print("Error: username is required.")
            return

        if not identity:
            password = input("Please enter your account password: ").strip()
            if not password:
                print("Error: password is required to proceed.")
                return
            config_json["password"] = password

        # Check and install `dfx`
        if not Tools.check_and_install_dfx():
            install_dfx()

        # Retrieve principal
        principal = get_principal(username)
        print('principal',principal)
        if not principal["status"]:
            print("Failed to retrieve principal ID.")
            return

        principal_id = principal["data"].get("principalId")
        if not identity:
            config_json["principalId"] = principal_id

        print(json.dumps(config_json, indent=2))

        # Validate configuration
        sample_auth_request = {"username": "", "password": ""}
        if identity:
            sample_auth_for_ii_request = {"identity": ""}
            valid_config = Tools.has_properties(config_json, sample_auth_for_ii_request.keys())
            if not valid_config:
                print('Invalid configuration data. Please run "quikdb config".')
                return
            print("Configuration data is valid for II.")
        else:
            valid_config = Tools.has_properties(config_json, sample_auth_request.keys())
            print('valid',valid_config)
            if not valid_config:
                print('Invalid configuration data. Please run "quikdb config".')
                return
            print("Configuration data is valid.")

        # Authenticate
        auth = authenticate_cli(config_json)
        if not auth["status"]:
            print("Failed to authenticate with the server.")
            return

        # Authenticate principal
        principal_auth = authenticate_principal(username, principal_id)
        if not principal_auth:
            return

        # Save seed phrase and access token
        if principal["data"].get("seedPhrase"):
            Tools.append_to_config_file(
                "seedPhrase",
                principal["data"]["seedPhrase"],
                Path(Tools.CONFIG_DIR) / "accessTokens"
            )
        Tools.append_to_config_file(
            "accessToken",
            auth["data"]["data"].get("accessToken"),
            Path(Tools.CONFIG_DIR) / "accessTokens"
        )

        # Fetch code and deploy locally
        shutil.rmtree("temp", ignore_errors=True)
        Tools.fetch_code("https://github.com/quikdb/quikdb-app-beta", "temp/quikdb")
        os.chdir("temp/quikdb")
        canister_url = deploy_to_local(principal_id)
        if not canister_url:
            return

        # Encrypt and upload project code
        payload = json.dumps({"id": auth["data"]["data"]["projectId"]})
        encryption_response = encrypt_user_data(payload, project_token_ref)
        print({"encryptionResponse": encryption_response["data"]["encryptedData"]})

        project_id = encryption_response["data"]["encryptedData"]
        token = auth["data"]["data"].get("accessToken")

        # Zip folder and upload
        os.chdir("../")
        folder_to_zip = "quikdb"
        zip_file_name = "dist.zip"
        with ZipFile(zip_file_name, "w") as zipf:
            for root, dirs, files in os.walk(folder_to_zip):
                for file in files:
                    zipf.write(os.path.join(root, file))
        print(f"Folder successfully zipped to {zip_file_name}")

        file_path = Path(__file__).parent.parent / "temp" / "dist.zip"
        upload_project_code(project_id, token, str(file_path))
    else:
        print("No configuration file found.")

# Add to CLI
# if __name__ == "__main__":
# install_command()
