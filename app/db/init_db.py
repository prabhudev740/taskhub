from db.crud.crud_permission import create_permissions
from schemas.user import CreateUser
from services.user_service import create_new_user


async def db_init():
    admin_data = CreateUser(
        first_name="admin",
        last_name="admin",
        username="admin",
        email="admin@gmail.com",
        password="admin@123"
    )
    await create_new_user(admin_data)
    await create_organization_permission()


async def create_organization_permission():
    organization_permissions = [
        {"name": "organization:read_details",
         "description": "View the organization's name, description, and settings."},
        {"name": "organization:update_settings",
         "description": "Update the organization's name, description, and settings."},
        {"name": "organization:delete", "description": "Delete the entire organization (typically owner-only)."},
        {"name": "organization:manage_members",
         "description": "Invite, remove, and view members of the organization."},
        {"name": "organization:manage_roles", "description": "Assign roles to members."},
        {"name": "organization:create_custom_roles",
         "description": "Create new custom roles within the organization."},
        {"name": "organization:manage_custom_roles",
         "description": "Edit and delete custom roles within the organization."},
        {"name": "organization:view_audit_log", "description": "View the organization's audit log."},
        {"name": "organization:manage_billing",
         "description": "View and manage billing information and subscription."},
    ]
    for perm in organization_permissions:
        create_permissions(permission_data=perm)