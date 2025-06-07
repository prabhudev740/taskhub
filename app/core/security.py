from fastapi.security import OAuth2PasswordBearer
from core.logging_conf import Logging
from passlib.context import CryptContext

log = Logging(__name__).log()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_hash_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)

def get_hashed_password(password):
    return pwd_context.hash(password)
