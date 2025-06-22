from pathlib import Path
import os

# Paths
PROJECT_PATH = Path(__file__).resolve().parent.parent.parent
BASE_PATH = Path(__file__).parent.parent

# Database
SQLITE_DATABASE_FILE = os.getenv("SQLITE_DATABASE_FILE", "taskhub.sql")
SQLITE_DATABASE_URL = f"sqlite:///{PROJECT_PATH / 'data'/ SQLITE_DATABASE_FILE}"
DATABASE_URL = os.getenv("DATABASE_URL", SQLITE_DATABASE_URL)

# Logger
EXECUTION_LOG_PATH = f"{PROJECT_PATH / 'execution.log'}"

# TODO: Try better approach to keep the secret
SECRET_KEY = os.getenv("SECRET_KEY", "4ba98d9b58410573bd6f583afb81e4a1b232528d64143fd0f6c15a8c26e96c04")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)

timezone = os.getenv("TIMEZONE", "utc")

