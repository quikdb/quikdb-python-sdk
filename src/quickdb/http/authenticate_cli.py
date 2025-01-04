import requests
from quickdb.utils.constants import SERVER_URL

def authenticate_cli(authentication_request: dict):
    """Send an authentication request to the server."""
    try:
        print("Authentication request!")
        if authentication_request.get('identity'):
            body = {
                'identity': authentication_request['identity'],
                'username': authentication_request['username'],
                'projectTokenRef': authentication_request['projectTokenRef'],
            }
        else:
            body = {
                'email': authentication_request['email'],
                'username': authentication_request['username'],
                'password': authentication_request['password'],
                'projectTokenRef': authentication_request['projectTokenRef'],
                'principalId': authentication_request['principalId'],
            }
        response = requests.post(f"{SERVER_URL}/a/signinWithCli", json=body)
        print('response',response.json())
        print(f"Authentication status: {response.status_code} {response.reason}")
        if response.status_code == 200:
            return {
                "status": True,
                "code": response.status_code,
                "data": response.json(),
            }
        else:
            return {
                "status": False,
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
