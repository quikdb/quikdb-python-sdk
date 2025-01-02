import requests
from pathlib import Path
from quickdb.utils.constants import SERVER_URL
from quickdb.file_types import LogStatus, StatusCode, LogAction

def upload_project_code(project_id: str, token: str, file_path: str):
    """Upload project code with a file attachment.

    Args:
        project_id (str): Encrypted project ID.
        token (str): Authorization token.
        file_path (str): Path to the file to be uploaded.

    Returns:
        dict: A structured response indicating the status of the upload.
    """
    try:
        # Ensure the file exists
        file = Path(file_path)
        if not file.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Prepare multipart form data
        with file.open("rb") as f:
            files = {"file": f}
            headers = {"Authorization": token}

            # Send PUT request
            response = requests.put(
                f"{SERVER_URL}/v/p/{project_id}/code",
                files=files,
                headers=headers,
            )

        # Return a structured success response
        return {
            "status": LogStatus.SUCCESS.value,
            "code": StatusCode.OK.value,
            "action": LogAction.UPLOAD_PROJECT_CODE.value,
            "message": "File upload success.",
            "data": response.json(),
        }
    except requests.exceptions.RequestException as error:
        error_response = getattr(error, "response", None)
        print("Error uploading project code:", error_response)
        # Return a structured error response
        return {
            "status": LogStatus.FAIL.value,
            "code": error_response.status_code if error_response else StatusCode.INTERNAL_SERVER_ERROR.value,
            "message": error_response.json().get("message") if error_response else "Internal server error.",
        }
    except FileNotFoundError as fnf_error:
        print(f"File error: {fnf_error}")
        return {
            "status": LogStatus.FAIL.value,
            "code": StatusCode.INTERNAL_SERVER_ERROR.value,
            "message": str(fnf_error),
        }
