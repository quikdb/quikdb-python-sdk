import requests
from quickdb.utils.constants import SERVER_URL

def authenticate_cli(authentication_request: dict):
    """Send an authentication request to the server."""
    try:
        print("Authentication request!")
        response = requests.post(f"{SERVER_URL}/a/signinWithCli", json=authentication_request)
        print(f"Authentication status: {response.status_code} {response.reason}")
        return {
            "status": True,
            "code": response.status_code,
            "data": response.json(),
        }
    except requests.exceptions.RequestException as error:
        print("Error sending deployment data to server:", error.response)
        return {
            "status": False,
            "code": error.response.status_code if error.response else None,
            "data": error.response.json() if error.response else None,
        }
