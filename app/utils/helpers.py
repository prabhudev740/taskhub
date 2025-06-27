from google.cloud import secretmanager


def get_secret(project_id: str, secret_id: str) -> secretmanager.GetSecretRequest:
    """
    Get information about the given secret. This only returns metadata about
    the secret container, not any secret material.
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Get the secret.
    response = client.get_secret(request={"name": name})

    # Get the replication policy.
    if "automatic" in response.replication:
        replication = "AUTOMATIC"
    elif "user_managed" in response.replication:
        replication = "MANAGED"
    else:
        raise Exception(f"Unknown replication {response.replication}")

    # Print data about the secret.
    print(f"Got secret {response.name} with replication policy {replication}")