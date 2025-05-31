from pathlib import Path


# Paths
BASE_PATH = Path(__file__).resolve().parent.parent.parent
APP_PATH = Path(__file__).parent.parent

# Database
SQLITE_DATABASE_FILE = "taskhub.sql"
DATABASE_URL = f"sqlite:///{BASE_PATH / 'data'/ SQLITE_DATABASE_FILE}"

# Todo: Auth - Try better approach to keep the secret
SECRET_KEY = "4ba98d9b58410573bd6f583afb81e4a1b232528d64143fd0f6c15a8c26e96c04"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

