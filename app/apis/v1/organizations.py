from uuid import UUID
from fastapi import APIRouter, Path, Query, status
from typing import Annotated
from schemas.organization import CreateOrganization, OrganizationResponse, AddOrganizationMembersRequest, \
    Organization, AddOrganizationMemberResponse
from services.organization_service import crate_new_organization, get_organization_details, \
    add_new_members_to_organization, verify_current_user_role
from services.user_service import CurrentActiveUserDep


router = APIRouter(prefix="/api/v1", tags=["organizations"])


@router.get("/organization", response_model=OrganizationResponse)
async def get_organization(current_user: CurrentActiveUserDep,
                           page: Annotated[int, Query(ge=1)] = 1,
                           size: Annotated[int, Query(ge=10)] = 10,
                           sort_by: Annotated[str, Query()] = "joined_at"):
    return await get_organization_details(current_user.id, page, size, sort_by)


@router.post("/organization", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(org: CreateOrganization,
                              current_user: CurrentActiveUserDep):
    return await crate_new_organization(org, current_user_id=current_user.id)


@router.get("/organization/{org_id}")
async def get_organization_by_id(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    ...


@router.put("/organization/{org_id}")
async def update_organization_by_id(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    ...


@router.delete("/organization/{org_id}")
async def delete_organization_by_id(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    ...


@router.get("/organization/{org_id}/members")
async def get_organization_members(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """ Get members of the organization id. """
    ...


@router.post("/organization/{org_id}/members", response_model=AddOrganizationMemberResponse)
async def add_member_to_organization(current_user: CurrentActiveUserDep,
                                   org_id: Annotated[str, Path(...)],
                                   user_roles: AddOrganizationMembersRequest):
    """ Invite / Add User """
    org_id = UUID(org_id)
    await verify_current_user_role(user_id=current_user.id,
                                   org_id=org_id,
                                   permission="organization:manage_members")
    return await add_new_members_to_organization(user_roles=user_roles)


@router.put("/organizations/{org_id}/members/{user_id}/role")
def get_members_role(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)], user_id: Annotated[str, Path(...)]):
    """ Assign/update a user's role within the organization. """
    ...


@router.delete("/organizations/{org_id}/members/{user_id}")
def remove_user_from_organization(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)], user_id: Annotated[str, Path(...)]):
    """ Remove a user from the organization. """
    ...


@router.get("/organizations/{org_id}/roles")
def get_x(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """ List available roles within the organization. """
    ...


@router.post("/organizations/{org_id}/roles")
def post_x(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """ Create a custom role within the organization (advanced ABAC). """
    ...


@router.get("/organizations/{org_id}/permissions")
def get_y(current_user: CurrentActiveUserDep, org_id: Annotated[str, Path(...)]):
    """ List available permissions for role definition. """
    ...
