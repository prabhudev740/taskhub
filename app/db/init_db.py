""" DB during setup"""

from core.logging_conf import Logging
from db.crud.crud_user import get_user_by_username
from schemas.user import CreateUser
from services.user_service import create_new_user


log = Logging(__name__).log()


async def db_init():
    """ Init the db while running for first time. """
    admin_data = CreateUser(
        first_name="admin",
        last_name="admin",
        username="admin",
        email="admin@gmail.com",
        password="admin@123",
    )
    if not get_user_by_username(username=admin_data.username):
        await create_new_user(admin_data, is_superuser=True)
