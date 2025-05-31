from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordBearer
from core.config import SECRET_KEY, ALGORITHM
from core.logging_conf import Logging
from passlib.context import CryptContext
import jwt

from db.models.user import UserInDB

log = Logging(__name__).log()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_hash_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)

def get_hashed_password(password):
    return pwd_context.hash(password)


fake_users_db = {
    "prabhu": {
        "username": "prabhu",
        "fullname": "Prabhuprasad Panda",
        "email": "prabhu@example.com",
        "hashed_password": get_hashed_password('prabhu123'),
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "fullname": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None



def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_hash_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
