from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthenticationRequestType:
    email: Optional[str] = None
    password: Optional[str] = None
    principal_id: str = ""
    identity: Optional[str] = None
    username: str = ""
    project_token_ref: str = ""

# Sample authentication requests
sample_auth_request = {
    "email": "example@example.com",
    "password": "example-password",
    "principal_id": "example-principal-id",
    "username": "example-username",
    "project_token_ref": "example-project-token-ref",
}

sample_auth_for_ii_request = {
    "identity": "example-identity-encrypted",
    "username": "example-username",
    "project_token_ref": "example-project-token-ref",
}
