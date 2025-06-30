""" Organization APIs """

from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Path, Query, status

from core.dependencies import CurrentActiveUserDep
from core.logging_conf import Logging
from schemas.organization import CreateOrganization, OrganizationResponse, Organization, \
    AddOrganizationMembersRequest, OrganizationMemberResponse, OrganizationByIDResponse, \
    UpdateOrganization, OrganizationMembersResponse, UpdateOrganizationMemberRole
from services.organization_service import crate_new_organization, get_organization_details, \
    add_new_members_to_organization, verify_current_user_role, get_organization_details_by_id, \
    update_organization_details, delete_organizations, get_organization_members_by_id, \
    update_organization_member_role_by_id, delete_member_from_organization

# Initialize API router for organization-related endpoints
router = APIRouter(prefix="/api/v1", tags=["organizations"])

log = Logging(__name__).log()


@router.get("/organization", response_model=OrganizationResponse)
async def get_organization(current_user: CurrentActiveUserDep,
                           page: Annotated[int, Query(ge=1)] = 1,
                           size: Annotated[int, Query(ge=10)] = 10,
                           sort_by: Annotated[str, Query()] = "joined_at"):
    """
    Retrieve a paginated list of organizations.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        page (int): Page number for pagination (minimum value: 1).
        size (int): Number of items per page (minimum value: 10).
        sort_by (str): Field to sort the organizations by.

    Returns:
        OrganizationResponse: Paginated list of organizations.
    """
    return await get_organization_details(current_user.id, page, size, sort_by)


@router.post("/organization", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(org: CreateOrganization, current_user: CurrentActiveUserDep):
    """
    Create a new organization.

    Args:
        org (CreateOrganization): Organization creation details.
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.

    Returns:
        Organization: Details of the newly created organization.
    """
    return await crate_new_organization(org, current_user_id=current_user.id)


@router.get("/organization/{org_id}", response_model=OrganizationByIDResponse)
async def get_organizations_by_id(current_user: CurrentActiveUserDep,
                                  org_id: Annotated[str, Path(...)]):
    """
    Retrieve organization details by ID.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization to retrieve.

    Returns:
        OrganizationByIDResponse: Details of the specified organization.
    """
    organization_id = UUID(org_id)
    await verify_current_user_role(user_id=current_user.id,
                                   org_id=organization_id,
                                   permission_names=["organization:read_details"])
    return await get_organization_details_by_id(org_id=organization_id, user=current_user)


@router.put("/organization/{org_id}", response_model=OrganizationByIDResponse)
async def update_organizations_by_id(current_user: CurrentActiveUserDep,
                                     org_id: Annotated[str, Path(...)],
                                     org: UpdateOrganization):
    """
    Update organization details by ID.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization to update.
        org (UpdateOrganization): Updated organization details.

    Returns:
        OrganizationByIDResponse: Updated organization details.
    """
    organization_id = UUID(org_id)
    await verify_current_user_role(user_id=current_user.id,
                                   org_id=organization_id,
                                   permission_names=["organization:update_settings"])
    return await \
        update_organization_details(organization_id=organization_id, org=org, user=current_user)


@router.delete("/organization/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organizations_by_id(current_user: CurrentActiveUserDep,
                                     org_id: Annotated[str, Path(...)]):
    """
    Delete an organization by ID.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization to delete.

    Returns:
        None: Indicates successful deletion.
    """
    organization_id = UUID(org_id)
    await verify_current_user_role(user_id=current_user.id,
                                   org_id=organization_id,
                                   permission_names=["organization:delete"])
    await delete_organizations(organization_id=organization_id)


@router.get("/organization/{org_id}/members", response_model=OrganizationMembersResponse)
async def get_organization_members(current_user: CurrentActiveUserDep,
                                   org_id: Annotated[str, Path(...)],
                                   page: Annotated[int, Query(ge=1)] = 1,
                                   size: Annotated[int, Query(ge=10)] = 10,
                                   sort_by: Annotated[str, Query()] = "joined_at"):
    """
    Retrieve members of an organization by ID.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization.
        page (int): Page number for pagination (minimum value: 1).
        size (int): Number of items per page (minimum value: 10).
        sort_by (str): Field to sort the organizations by.

    Returns:
        Any: List of organization members (to be implemented).
    """
    log.info("%s %s", current_user.id, org_id)
    organization_id =UUID(org_id)
    return await get_organization_members_by_id(organization_id=organization_id,
                                                page=page, size=size, sort_by=sort_by)


@router.post("/organization/{org_id}/members", response_model=list[OrganizationMemberResponse])
async def add_member_to_organization(current_user: CurrentActiveUserDep,
                                   org_id: Annotated[str, Path(...)],
                                   user_roles: AddOrganizationMembersRequest):
    """
    Add or invite a user to an organization.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization.
        user_roles (AddOrganizationMembersRequest): Roles and details of the user to add.

    Returns:
        OrganizationMemberResponse: Response indicating the result of the operation.
    """
    org_id = UUID(org_id)
    await verify_current_user_role(user_id=current_user.id,
                                   org_id=org_id,
                                   permission_names=['organization:manage_members',
                                                     'organization:manage_roles',])
    return await add_new_members_to_organization(user_roles=user_roles, organization_id=org_id)


@router.put("/organizations/{org_id}/members/{user_id}/role",
            response_model=OrganizationMemberResponse)
async def update_members_role(current_user: CurrentActiveUserDep,
                        org_id: Annotated[str, Path(...)],
                        user_id: Annotated[str, Path(...)],
                        update_role: UpdateOrganizationMemberRole):
    """
    Assign or update a user's role within an organization.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization.
        user_id (str): ID of the user whose role is being updated.
        update_role (UpdateOrganizationMemberRole): Contains the role_id to be updated.

    Returns:
        Any: Result of the role update operation (to be implemented).
    """
    log.info("%s %s %s", current_user.id, org_id, user_id)
    org_id, user_id = UUID(org_id), UUID(user_id)
    await verify_current_user_role(user_id=current_user.id,
                                   org_id=org_id,
                                   permission_names=["organization:manage_roles"])
    return await update_organization_member_role_by_id(org_id=org_id,
                                                    user_id=user_id, role_id=update_role.role_id)


@router.delete("/organizations/{org_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_from_organization(current_user: CurrentActiveUserDep,
                                  org_id: Annotated[str, Path(...)],
                                  user_id: Annotated[str, Path(...)]):
    """
    Remove a user from an organization.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): The ID of the organization.
        user_id (str): The ID of the user to remove.

    Returns:
        None: Indicates successful deletion.
    """
    log.info("%s %s %s", current_user.id, org_id, user_id)
    user_id, org_id = UUID(user_id), UUID(org_id)
    await verify_current_user_role(user_id=user_id, org_id=org_id,
                                   permission_names=['organization:manage_members'])
    await delete_member_from_organization(user_id=user_id, organization_id=org_id)


@router.get("/organizations/{org_id}/roles")
def get_x(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """
    List available roles within an organization.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization.

    Returns:
        Any: List of roles (to be implemented).
    """
    log.info("%s %s", current_user.id, org_id)


@router.post("/organizations/{org_id}/roles")
def post_x(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """
    Create a custom role within an organization.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization.

    Returns:
        Any: Result of the role creation operation (to be implemented).
    """
    log.info("%s %s", current_user.id, org_id)


@router.get("/organizations/{org_id}/permissions")
def get_y(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """
    List available permissions for role definition within an organization.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization.

    Returns:
        Any: List of permissions (to be implemented).
    """
    log.info("%s %s", current_user.id, org_id)


@router.put("/organizations/{org_id}/permissions")
def update_role_permission(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """
    Update permissions for role definition within an organization.

    Args:
        current_user (CurrentActiveUserDep): Dependency to fetch the currently authenticated user.
        org_id (str): ID of the organization.

    Returns:
        Any: Result of the permission update operation (to be implemented).
    """
    log.info("%s %s", current_user.id, org_id)
