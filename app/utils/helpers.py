""" The Helpers file."""
from typing import Annotated
from uuid import UUID
from fastapi import Path
from core.logging_conf import Logging


log = Logging(__name__).log()

# from google.cloud import secretmanager
#
#
# def get_secret(project_id: str, secret_id: str) -> secretmanager.GetSecretRequest:
#     """
#     Retrieve metadata about a secret from Google Cloud Secret Manager.
#
#     Args:
#         project_id (str): The ID of the Google Cloud project containing the secret.
#         secret_id (str): The ID of the secret to retrieve.
#
#     Returns:
#         secretmanager.GetSecretRequest: Metadata about the secret container.
#
#     Raises:
#         Exception: If the replication policy is unknown.
#
#     Example:
#         >>> get_secret("my-project", "my-secret")
#     """
#
#     # Import the Secret Manager client library.
#     from google.cloud import secretmanager
#
#     # Create the Secret Manager client.
#     client = secretmanager.SecretManagerServiceClient()
#
#     # Build the resource name of the secret.
#     name = client.secret_path(project_id, secret_id)
#
#     # Get the secret metadata.
#     response = client.get_secret(request={"name": name})
#
#     # Determine the replication policy.
#     if "automatic" in response.replication:
#         replication = "AUTOMATIC"
#     elif "user_managed" in response.replication:
#         replication = "MANAGED"
#     else:
#         raise Exception(f"Unknown replication {response.replication}")
#
#     # Print metadata about the secret.
#     print(f"Got secret {response.name} with replication policy {replication}")


def get_organization_id(organization_id: Annotated[str, Path(...)]) -> UUID:
    """
    Coverts the str organization id to UUID.

    Args:
        organization_id (str): The organization_id in String type.

    Returns:
        UUID: organization_id in UUID.
    """
    return UUID(organization_id)


def get_team_id(team_id: Annotated[str, Path(...)]) -> UUID:
    """
    Coverts the str organization id to UUID.

    Args:
        team_id (str): The team_id in String type.

    Returns:
        UUID: team_id in UUID.
    """
    return UUID(team_id)
