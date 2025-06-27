""" Security """
from fastapi.security import OAuth2PasswordBearer
from core.logging_conf import Logging
from passlib.context import CryptContext


# Initialize logger for the module
log = Logging(__name__).log()

# Define the OAuth2 password bearer scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Configure the password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_hash_password(plane_password, hashed_password):
    """
    Verify if a plain password matches its hashed counterpart.

    Args:
        plane_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plane_password, hashed_password)

def get_hashed_password(password):
    """
    Hash a plain password using the configured hashing context.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)
