import requests
from quickdb.utils.constants import SERVER_URL
from quickdb.file_types import LogStatus, StatusCode

def activate_project(project_id: str, payload: str, access_token: str):
    """
    Function to encrypt user data by making a POST request to /v/p/projectId/activate.
    """
    try:
        url = f"{SERVER_URL}/v/p/{project_id}/activate"
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json",
        }
        response = requests.post(url, json={"data": payload}, headers=headers)

        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        
        return {
            "status": LogStatus.SUCCESS,
            "code": StatusCode.OK,
            "message": "Data encrypted successfully.",
            "data": response.json().get("data"),
        }
    except requests.exceptions.RequestException as e:
        error_response = getattr(e.response, 'json', lambda: {})()
        return {
            "status": LogStatus.FAIL,
            "code": e.response.status_code if e.response else 500,
            "message": error_response.get("message", "Internal server error."),
        }
