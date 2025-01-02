import requests
from quickdb.utils.constants import SERVER_URL
from quickdb.file_types import LogStatus, StatusCode  # Assuming these are defined as enums in Python

def encrypt_user_data(payload: str, project_token_ref: str):
    """Encrypt user data by making a POST request to /a/encrypt."""
    try:
        response = requests.post(
            f"{SERVER_URL}/a/encrypt",
            json={"data": payload},
            headers={
                "Authorization": project_token_ref,
                "Content-Type": "application/json",
            },
        )
        # Return a structured response
        return {
            "status": LogStatus.SUCCESS,
            "code": StatusCode.OK,
            "message": "Data encrypted successfully.",
            "data": response.json().get("data"),
        }
    except requests.exceptions.RequestException as error:
        # Handle errors and return a structured response
        error_response = getattr(error, "response", None)
        print(
            "Error encrypting user data:",
            error_response.json() if error_response else str(error),
        )

        return {
            "status": LogStatus.FAIL,
            "code": error_response.status_code if error_response else 500,
            "message": error_response.json().get("message") if error_response else "Internal server error.",
        }
