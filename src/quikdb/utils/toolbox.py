import os
import json
from pathlib import Path
import subprocess
import shutil

class Tools:
    CONFIG_DIR = Path.home() / '.quikdb'
    CONFIG_FILE = CONFIG_DIR / 'config'

    @staticmethod
    def ensure_config_directory():
        """Ensure the configuration directory exists."""
        if not Tools.CONFIG_DIR.exists():
            Tools.CONFIG_DIR.mkdir(parents=True)
            print(f"Created config directory: {Tools.CONFIG_DIR}")

    @staticmethod
    def append_to_config_file(key: str, value: str, file_path: str = None):
        """Append a key-value pair to the configuration file."""
        Tools.ensure_config_directory()
        config_entry = f"{key}& {value}\n"

        target_file = Path(file_path) if file_path else Tools.CONFIG_FILE
        try:
            with target_file.open('a') as f:
                f.write(config_entry)
            print(f"Appended to config: {key} = {value}")
        except Exception as error:
            print(f"Error appending to configuration file: {error}")

    @staticmethod
    def get_config_as_json(config_data: str) -> dict:
        """Convert configuration file data to JSON."""
        config_json = {}
        lines = config_data.split('\n')

        for line in lines:
            if line.strip():
                key, value = map(str.strip, line.split(':', 1))
                if key and value:
                    config_json[key] = value

        return config_json

    @staticmethod
    def is_of_type(obj, type_check):
        """Check if an object matches a given type using a type-checking function."""
        return type_check(obj)

    @staticmethod
    def has_properties(obj, properties):
        """Check if an object has the given properties."""
        return (hasattr(obj, prop) for prop in properties)

    @staticmethod
    def check_and_install_dfx():
        """Check if `dfx` is installed and install if necessary."""
        if shutil.which('dfx'):
            print('dfx is already installed on your system.')
            return True
        else:
            print('dfx not found. Installing dfx...')
            return False

    @staticmethod
    def fetch_code(repo: str, local_path: str):
        """Clone a repository to the local path."""
        print(f"Cloning repository from {repo}...")
        subprocess.run(['git', 'clone', repo, local_path], check=True)
        print('Repository cloned successfully.')

    @staticmethod
    def parse_url(url: str) -> dict:
        """
        Splits the URL at '?', capturing the baseUrl and query params.
        Looks specifically for 'canisterId' and 'id' in the query string.
        """
        split_url = url.split("?", 1)
        base_url = split_url[0]
        if len(split_url) == 1:
            return {"baseUrl": base_url, "canisterId": "", "id": ""}

        query_string = split_url[1]
        params = query_string.split("&")
        canister_id = ""
        _id = ""

        for param in params:
            key_val = param.split("=")
            if len(key_val) == 2:
                key, val = key_val
                if key == "canisterId":
                    canister_id = val
                elif key == "id":
                    _id = val

        return {"baseUrl": base_url, "canisterId": canister_id, "id": _id}
