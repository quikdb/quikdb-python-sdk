import shutil
import subprocess
import re
from quickdb.utils.constants import production

def create_principal(username: str):
    """Create a new principal using dfx."""
    if not shutil.which("dfx"):
        print("dfx is not installed. Please run `quikdb install-dfx` first.")
        return {"status": False}

    print("Creating new principal...")
    try:
        result = subprocess.run(
            ["dfx", "identity", "new", username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            
        )

        if result.returncode != 0:
            print("Error creating identity.")
            return {"status": False}
        
        
        # Extract seed phrase using regex
        print("results", result)
        print("results", type(result.stdout))
        seed_phrase_match = re.search(r"Your seed phrase for identity '[^']+': (.*)", result.stderr)
        seed_phrase = seed_phrase_match.group(1).strip() if seed_phrase_match else None

        if not seed_phrase:
            print("Error extracting seed phrase.")
            return {"status": False}

        return {"status": True, "seedPhrase": seed_phrase}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"status": False}
