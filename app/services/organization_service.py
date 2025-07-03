""" Org Service """
from uuid import UUID
from fastapi import HTTPException, status
from core.logging_conf import Logging
from core.permission_config import ORGANIZATION_ROLES, ALL_PERMISSIONS
from db.crud.crud_organization import get_organization_by_name, update_organization_member, \
    get_organizations_by_member_id, get_organization_by_id, create_organization, \
    get_organization_member_count_by_organization_id, delete_organizations_by_id, \
    get_organization_member_by_organization_user_id, get_organization_members_by_organization_id, \
    update_organization, update_organization_member_role, delete_organization_member_by_id
from db.crud.crud_permission import get_permission_by_name, get_permission_by_id, create_permissions
from db.crud.crud_user import get_user_by_username, get_user_by_id
from db.crud.curd_role import get_role_permission, get_role_by_id, create_role, \
    update_role_permission, get_role_by_role_name_org_id, get_all_organization_roles, \
    get_permission_ids_for_role
from exceptions import http_exceptions
from schemas.organization import CreateOrganization, Organization, OrganizationResponse, \
    AddOrganizationMembersRequest, OrganizationMemberResponse, OrganizationByIDResponse, \
    UpdateOrganization, OrganizationMembersResponse, OrganizationMemberData
from schemas.role import RoleShort, RoleResponse, CreateCustomRole, CreateRole, Permission, \
    AllRoleResponse, Role, PermissionsResponse
from schemas.user import UserProfileShort, User


log = Logging(__name__).log()

async def map_role_permissions(role_id: UUID, permissions: list[str | UUID]) -> None:
    """
    Update the role_permission table.

    Args:
        role_id (UUID): The ID of the role.
        permissions (list[str | UUID]): List of permissions (names or UUIDs)

    Raises:
        HTTPException: If invalid permission Name of ID provided.
    """
    if not permissions:
        return None
    permission = permissions[0]
    if isinstance(permission, str):
        permission = get_permission_by_name(permission_name=permission)
    else:
        permission = get_permission_by_id(permission_id=permission)

    if not permission:
        raise http_exceptions.PERMISSION_NOT_FOUND_EXCEPTION
    update_role_permission(role_id=role_id, permission_id=permission.id)
    return await map_role_permissions(role_id=role_id, permissions=permissions[1:])


async def create_default_organization_role_permissions(organization_id: UUID):
    """
    Create Default roles and permissions the for the organization.

    Args:
        organization_id (UUID): The ID of the organization.
    """
    # Create permissions only if not present
    for perm in ALL_PERMISSIONS:
        if not get_permission_by_name(permission_name=perm['name']):
            create_permissions(permission_data=perm)

    # Create roles and assign permissions only if role not present
    for role_data in ORGANIZATION_ROLES.values():
        if not get_role_by_role_name_org_id(role_data['name'], org_id=organization_id):
            role = CreateRole(name=role_data['name'], description=role_data['description'],
                              organization_id=organization_id)
            role = role.model_dump(exclude_unset=True)
            created_role = create_role(role)
            role_id = created_role.id
            await map_role_permissions(role_id, role_data['permissions'])


async def add_new_organization_member(current_user_id, organization_id, role_name: str):
    """
    Add a new member to an organization.

    Args:
        current_user_id: The ID of the current user.
        organization_id: The ID of the organization.
        role_name (str): The name of the role to assign to the user.

    Returns:
        dict: The updated organization member data.

    Raises:
        HTTPException: If the specified role is not found.
    """
    role_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Given role not found."
    )
    role = get_role_by_role_name_org_id(role_name=role_name, org_id=organization_id)
    if not role:
        raise role_not_found_exception
    organization_member = {"user_id": current_user_id,
                           "organization_id": organization_id, "role_id": role.id}
    return update_organization_member(organization_member)


async def crate_new_organization(org: CreateOrganization, current_user_id: UUID) -> Organization:
    """
    Create a new organization and assign the current user as the owner.

    Args:
        org (CreateOrganization): The organization creation data.
        current_user_id (UUID): The ID of the current user.

    Returns:
        Organization: The created organization.

    Raises:
        HTTPException: If the organization name already exists.
    """
    if get_organization_by_name(org.name):
        raise http_exceptions.ORGANIZATION_ALREADY_EXISTS_EXCEPTION
    organization_data = org.model_dump(exclude_unset=True)
    organization_data.update({"owner_id": current_user_id})
    organization = create_organization(organization_data)
    await create_default_organization_role_permissions(organization_id=organization.id)
    await add_new_organization_member(current_user_id, organization.id, "Owner")
    return Organization.model_validate(organization)


async def get_organization_details(user_id: UUID, page: int,
                                   size: int, sort_by: str
                                   ) -> OrganizationResponse:
    """
    Retrieve paginated organization details for a user.

    Args:
        user_id (UUID): The ID of the user.
        page (int): The page number for pagination.
        size (int): The number of items per page.
        sort_by (str): The field to sort the organizations by.

    Returns:
        OrganizationResponse: The paginated organization details.
    """
    items, total, pages = get_organizations_by_member_id(user_id=user_id, page=page,
                                                         size=size, sort_by=sort_by)
    organizations = list(map(Organization.model_validate, items))
    organizations_response = OrganizationResponse(items=organizations, total=total,
                                                  pages=pages, page=page, size=size)
    return organizations_response


def update_organization_response(organization_id: UUID, organization: Organization,
                                 user: User) -> OrganizationByIDResponse:
    """
    Update the organization response with additional details.

    Args:
        organization_id (UUID): The ID of the organization.
        organization (Organization): The organization data.
        user (User): The user data.

    Returns:
        OrganizationByIDResponse: The updated organization response.
    """
    response = organization.model_dump(exclude_unset=True)
    response["owner_details"] = UserProfileShort(id=user.id,
                                                 email=user.email,
                                                 full_name=f"{user.first_name} {user.last_name}")
    response["member_count"] = \
        get_organization_member_count_by_organization_id(org_id=organization_id)
    return OrganizationByIDResponse.model_validate(response)

async def get_organization_details_by_id(org_id: UUID, user: User) -> OrganizationByIDResponse:
    """
    Retrieve organization details by its ID.

    Args:
        org_id (UUID): The ID of the organization.
        user (User): The user data.

    Returns:
        OrganizationByIDResponse: The organization details.

    Raises:
        HTTPException: If the organization is not found.
    """
    organization = get_organization_by_id(organization_id=org_id)
    if not organization:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION

    organization_data = Organization.model_validate(organization)
    return update_organization_response(organization_id=org_id,
                                        organization=organization_data,
                                        user=user)

async def get_verified_role_permissions(role_id: UUID, permission_names: list[str]):
    """
    Verify and retrieve the permission associate with given role ID.

    Args:
        role_id (UUID): The ID of the role.
        permission_names (list[str]): The list of names of the permissions.

    Returns:
        Any: The role permission data.
    """
    if not permission_names:
        return []

    permission_name = permission_names.pop()
    permission = get_permission_by_name(permission_name=permission_name)
    if not permission:
        raise http_exceptions.PERMISSION_NOT_FOUND_EXCEPTION

    role_permission = get_role_permission(role_id=role_id, permission_id=permission.id)
    if not role_permission:
        raise http_exceptions.FORBIDDEN_EXCEPTION

    return await get_verified_role_permissions(role_id, permission_names) + [role_permission]

async def verify_current_user_role(user_id: UUID, org_id: UUID, permission_names: list[str]):
    """
    Verify the current user's role and permissions in an organization.

    Args:
        user_id (UUID): The ID of the user.
        org_id (UUID): The ID of the organization.
        permission_names (list[str]): The list of names of the permission to verify.

    Returns:
        Any: The role permission data.

    Raises:
        HTTPException: If the organization, permission, or role permission is not found.
    """

    log.info("org_id=%s, user_id=%s", org_id, user_id)
    organization_member = \
        get_organization_member_by_organization_user_id(org_id=org_id, user_id=user_id)
    if not organization_member:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION
    role_permissions = await get_verified_role_permissions(role_id=organization_member.role_id,
                                                           permission_names=permission_names)
    return role_permissions


async def update_organization_details(organization_id: UUID, org: UpdateOrganization,
                                      user: User) -> OrganizationByIDResponse:
    """
    Update the details of an organization.

    Args:
        organization_id (UUID): The ID of the organization.
        org (UpdateOrganization): The updated organization data.
        user (User): The user data.

    Returns:
        OrganizationByIDResponse: The updated organization details.

    Raises:
        HTTPException: If the organization is not found.
    """
    organization_data = org.model_dump(exclude_unset=True)
    organization = update_organization(organization_id=organization_id, org=organization_data)
    if not organization:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION

    organization_data = Organization.model_validate(organization)
    return update_organization_response(organization_id=organization_id,
                                        organization=organization_data,
                                        user=user)

async def delete_organizations(organization_id: UUID) -> None:
    """
    Delete an organization by its ID.

    Args:
        organization_id (UUID): The ID of the organization.

    Raises:
        HTTPException: If the organization is not found.
    """
    deleted = delete_organizations_by_id(organization_id=organization_id)
    if not deleted:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION


async def add_new_members_to_organization(organization_id: UUID,
                                          user_roles: AddOrganizationMembersRequest
                                          ) -> list[OrganizationMemberResponse]:
    """
    Add new members to an organization.

    Args:
        organization_id (UUID): The ID of the organization.
        user_roles (AddOrganizationMembersRequest): The user roles to add.

    Returns:
        list[OrganizationMemberResponse]: The list of added organization members.

    Raises:
        HTTPException: If the user, role, or membership already exists.
    """
    if not user_roles.user_roles:
        return []

    user_role = user_roles.user_roles[0]
    remaining_roles = AddOrganizationMembersRequest(user_roles=user_roles.user_roles[1:])

    user = get_user_by_username(username=user_role.username)
    if not user:
        raise http_exceptions.USER_NOT_FOUND_EXCEPTION
    existing_member = get_organization_member_by_organization_user_id(org_id=organization_id,
                                                                      user_id=user.id)
    if existing_member:
        raise http_exceptions.ALREADY_MEMBER_EXCEPTION
    role = get_role_by_role_name_org_id(role_name=user_role.role_name, org_id=organization_id)
    if not role:
        raise http_exceptions.ROLE_NOT_FOUND_EXCEPTION

    organization_member = \
        {"user_id": user.id, "organization_id": organization_id, "role_id": role.id}
    created_user = update_organization_member(organization_member)
    current_response = OrganizationMemberResponse(
        user_id=user.id,
        organization_id=organization_id,
        role_id=role.id,
        role_name=role.name,
        user_email=user.email,
        user_full_name=f"{user.first_name} {user.last_name}",
        status="active",
        joined_at=created_user.joined_at
    )

    rest_responses = await add_new_members_to_organization(organization_id, remaining_roles)
    return [current_response] + rest_responses


async def get_organization_members_by_id(organization_id: UUID, page: int,
                                         size: int, sort_by: str) -> OrganizationMembersResponse:
    """
     Retrieves list of members by organization_id.

     Args:
         organization_id (UUID): The ID of the organization.
         page (int): The page number for pagination.
         size (int): The number of items per page.
         sort_by (str): The field to sort the organizations by.

    Returns:
        OrganizationMembersResponse: Organization member details.

    Raises:
        HTTPException: If the organization is not found.
     """
    organization = get_organization_by_id(organization_id=organization_id)
    if not organization:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION

    items, total, pages = get_organization_members_by_organization_id(
        organization_id=organization_id, page=page, size=size, sort_by=sort_by)
    members = []
    for item in items:
        member = {}
        user = get_user_by_id(item.user_id)
        if not user:
            raise http_exceptions.USER_NOT_FOUND_EXCEPTION

        role = get_role_by_id(role_id=item.role_id)
        if not role:
            raise http_exceptions.ROLE_NOT_FOUND_EXCEPTION

        member['user'] = UserProfileShort(id=user.id, email=user.email,
                                          full_name=f"{user.first_name} {user.last_name}")
        member['role'] = RoleShort(id=role.id, name=role.name)
        member['joined_at'] = item.joined_at
        members.append(OrganizationMemberData.model_validate(member))

    return OrganizationMembersResponse(items=members,
                                          total=total, page=page, size=size, pages=pages)


async def update_organization_member_role_by_id(org_id: UUID, user_id: UUID, role_id: UUID
                                                ) -> OrganizationMemberResponse:
    """
    Update the role of a specific member within an organization.

    Args:
        org_id (UUID): The ID of the organization.
        user_id (UUID): The ID of the user whose role is being updated.
        role_id (UUID): The new role ID to assign to the user.

    Returns:
        OrganizationMemberResponse: The updated organization member details.

    Raises:
        HTTPException: If the organization member, role, or user is not found.
    """
    org_member = update_organization_member_role(org_id=org_id, user_id=user_id, role_id=role_id)
    if not org_member:
        raise http_exceptions.ORGANIZATION_MEMBER_NOT_FOUND_EXCEPTION

    role = get_role_by_id(role_id=org_member.role_id)
    if not role:
        raise http_exceptions.ROLE_NOT_FOUND_EXCEPTION

    user = get_user_by_id(user_id=org_member.user_id)
    if not user:
        raise http_exceptions.USER_NOT_FOUND_EXCEPTION

    current_response = OrganizationMemberResponse(
        user_id=org_member.user_id,
        organization_id=org_member.organization_id,
        role_id=role_id,
        role_name=role.name,
        user_email=user.email,
        user_full_name=f"{user.first_name} {user.last_name}",
        status="active",
        joined_at=org_member.joined_at
    )
    return OrganizationMemberResponse.model_validate(current_response)


async def delete_member_from_organization(user_id: UUID, organization_id: UUID) -> None:
    """
    Remove the user from the organization.

    Args:
        user_id (UUID): The ID of user to remove.
        organization_id (UUID): The ID of organization where user to be removed.

    Raises:
        HTTPException: If the organization is not found.
    """
    deleted = delete_organization_member_by_id(user_id=user_id, organization_id=organization_id)
    if not deleted:
        raise http_exceptions.ORGANIZATION_MEMBER_NOT_FOUND_EXCEPTION


async def get_permission_response(permission_id: UUID) -> dict:
    """
    Retrieve the permission by permission ID and return as dict

    Args:
        permission_id (UUID): The ID of the permission needs to br retrieved.

    Returns:
        dict: Returns the validated dict.
    """
    permission = get_permission_by_id(permission_id=permission_id)
    if not permission:
        raise http_exceptions.PERMISSION_NOT_FOUND_EXCEPTION
    permission_data = {
            "id": permission.id,
            "name": permission.name,
            "description": permission.description
        }
    return permission_data

async def get_permissions_response(permission_ids: list[UUID]) -> list[dict] | list[Permission]:
    """
    Retrieve list of all Permissions defined in the organization.
    Args:
        permission_ids (list[UUID]): List of permission IDs.

    Returns:
        list[dict] | list[Permission]: List of permission as Permission object or dict object.
    """
    permissions = []
    for permission_id in permission_ids:
        permission = await get_permission_response(permission_id=permission_id)
        permissions.append(Permission.model_validate(permission))
    return permissions


async def get_role_response(role: Role, permission_ids: list[UUID]) -> dict:
    """
    Generate the Role Response for given role and permission ids.

    Args:
        role (Role): The Role object for creating response.
        permission_ids (list[UUID]): Permission ids to create response.

    Raises:
        HTTPException: If a permission ID is not present in the organization.

    Returns:
        dict: The Role response.
    """
    permissions = await get_permissions_response(permission_ids=permission_ids)
    response_role = {
      "id": role.id,
      "name": role.name,
      "description": role.description,
      "organization_id": role.organization_id,
      "is_system_role": role.is_system_role,
      "permissions": permissions
    }
    return response_role


async def create_new_role(organization_id: UUID, new_role: CreateCustomRole
                          ) -> RoleResponse:
    """
    Create a new custom role for the organization.

    Args:
        organization_id (UUID): The ID of the organization.
        new_role (CreateCustomRole): Role data to create a custom role.

    Raises:
        HTTPException: Permission not found or Role already exists.

    Returns:
        RoleResponse: The response after organization creation.
    """
    existing_role = get_role_by_role_name_org_id(role_name=new_role.name, org_id=organization_id)
    if existing_role and existing_role.organization_id == organization_id:
        raise http_exceptions.ROLE_ALREADY_EXITS_EXCEPTION
    role_data = CreateRole(name=new_role.name, description=new_role.description,
                           organization_id=organization_id)
    role_dict = role_data.model_dump(exclude_unset=True)
    created_role = create_role(role=role_dict)
    role = Role.model_validate(created_role)
    await map_role_permissions(role_id=created_role.id, permissions=new_role.permission_ids)
    response_role = await get_role_response(role=role, permission_ids=new_role.permission_ids)
    return RoleResponse.model_validate(response_role)


async def get_organization_roles(organization_id: UUID) -> AllRoleResponse:
    """
    Retrieve the Roles for the given organization ID

    Args:
        organization_id (UUID): The ID of the organization.

    Raises:
        HTTPException: If Permission not found in organization.

    Returns:
         AllRoleResponse: the list of RoleResponse.
    """
    roles = get_all_organization_roles(organization_id=organization_id)
    response_roles = []
    for role in roles:
        permission_ids = get_permission_ids_for_role(role_id=role.id)
        response_role = await get_role_response(role=role, permission_ids=permission_ids)
        response_roles.append(response_role)
    response = {"items": response_roles}
    return AllRoleResponse.model_validate(response)


async def get_all_permissions(organization_id: UUID) -> PermissionsResponse:
    """
    Get all permissions for given organization ID.
    Args:
        organization_id (UUID): The ID of the organization.

    Returns:
        PermissionsResponse: Schema validated permission response.
    """
    roles = get_all_organization_roles(organization_id=organization_id)
    response_permissions = []
    for role in roles:
        permission_ids = get_permission_ids_for_role(role_id=role.id)
        permission_ids = list(set(permission_ids))
        response_permission = await get_permissions_response(permission_ids=permission_ids)
        response_permissions.extend(response_permission)
    response = {"items": response_permissions, "total": len(response_permissions)}
    return PermissionsResponse.model_validate(response)
