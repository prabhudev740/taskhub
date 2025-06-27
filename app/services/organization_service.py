from uuid import UUID
from fastapi import HTTPException, status
from watchfiles import awatch

from core.logging_conf import Logging
from db.crud.crud_organization import get_organization_by_name, update_organization_member, \
    get_organizations_by_member_id, get_organization_by_id, create_organization, \
    get_organization_member_by_organization_id, get_organization_member_by_organization_user_id, update_organization, \
    delete_organizations_by_id
from db.crud.crud_permission import get_permission_by_name
from db.crud.crud_user import get_user_by_username
from db.crud.curd_role import get_role_by_name, get_role_permission
from exceptions import http_exceptions
from schemas.organization import CreateOrganization, Organization, OrganizationResponse, \
    AddOrganizationMembersRequest, AddOrganizationMemberResponse, OrganizationByIDResponse, UpdateOrganization, \
    OrganizationMessageResponse
from schemas.user import UserProfileShort, User


log = Logging(__name__).log()


async def add_new_organization_member(current_user_id, organization_id, role_name: str):
    role_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Given role not found."
    )
    role = get_role_by_name(role_name=role_name)
    if not role:
        raise role_not_found_exception
    organization_member = {"user_id": current_user_id,
                           "organization_id": organization_id, "role_id": role.id}
    return update_organization_member(organization_member)


async def crate_new_organization(org: CreateOrganization, current_user_id: UUID) -> Organization:
    if get_organization_by_name(org.name):
        raise http_exceptions.ORGANIZATION_ALREADY_EXISTS_EXCEPTION
    organization_data = org.model_dump(exclude_unset=True)
    organization_data.update({"owner_id": current_user_id})
    organization = create_organization(organization_data)
    await add_new_organization_member(current_user_id, organization.id, "Owner")
    return Organization.model_validate(organization)


async def get_organization_details(user_id: UUID, page: int,
                                   size: int, sort_by: str
                                   ) -> OrganizationResponse:
    items, total, pages = get_organizations_by_member_id(user_id=user_id, page=page,
                                                         size=size, sort_by=sort_by)
    organizations = list(map(Organization.model_validate, items))
    organizations_response = OrganizationResponse(items=organizations, total=total,
                                                  pages=pages, page=page, size=size)
    return organizations_response


def update_organization_response(organization_id: UUID, organization: Organization,
                                 user: User) -> OrganizationByIDResponse:
    response = organization.model_dump(exclude_unset=True)
    response["owner_details"] = UserProfileShort(id=user.id,
                                                 email=user.email,
                                                 full_name=f"{user.first_name} {user.last_name}")
    response["member_count"] = get_organization_member_by_organization_id(org_id=organization_id)
    return OrganizationByIDResponse.model_validate(response)

async def get_organization_details_by_id(org_id: UUID, user: User) -> OrganizationByIDResponse:
    organization = get_organization_by_id(organization_id=org_id)
    if not organization:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION

    organization_data = Organization.model_validate(organization)
    return update_organization_response(organization_id=org_id,
                                        organization=organization_data,
                                        user=user)


async def verify_current_user_role(user_id: UUID, org_id: UUID, permission_name: str):
    permission_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to perform this action."
    )
    organization_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Organization associated to current user not found."
    )
    permission_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Organization associated to current user not found."
    )
    log.info("org_id=%s, user_id=%s", org_id, user_id)
    organization_member = \
        get_organization_member_by_organization_user_id(org_id=org_id, user_id=user_id)
    if not organization_member:
        raise organization_not_found_exception

    permission = get_permission_by_name(permission_name=permission_name)
    if not permission:
        raise permission_not_found_exception

    role_permission = \
        get_role_permission(role_id=organization_member.role_id, permission_id=permission.id)
    if not role_permission:
        raise permission_exception

    return role_permission


async def update_organization_details(organization_id: UUID, org: UpdateOrganization,
                                user: User) -> OrganizationByIDResponse:
    organization_data = org.model_dump(exclude_unset=True)
    organization = update_organization(organization_id=organization_id, org=organization_data)
    if not organization:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION

    organization_data = Organization.model_validate(organization)
    return update_organization_response(organization_id=organization_id,
                                        organization=organization_data,
                                        user=user)

async def delete_organizations(organization_id: UUID) -> None:
    deleted = delete_organizations_by_id(organization_id=organization_id)
    if not deleted:
        raise http_exceptions.ORGANIZATION_NOT_FOUND_EXCEPTION


async def add_new_members_to_organization(organization_id: UUID,
                                          user_roles: AddOrganizationMembersRequest
                                          ) -> list[AddOrganizationMemberResponse]:
    if not user_roles.user_roles:
        return list()

    user_role = user_roles.user_roles[0]
    remaining_roles = AddOrganizationMembersRequest(user_roles=user_roles.user_roles[1:])

    user = get_user_by_username(username=user_role.username)
    if not user:
        raise http_exceptions.USER_NOT_FOUND_EXCEPTION
    existing_member = get_organization_member_by_organization_user_id(org_id=organization_id,
                                                                      user_id=user.id)
    if existing_member:
        raise http_exceptions.ALREADY_MEMBER_EXCEPTION
    role = get_role_by_name(role_name=user_role.role_name)
    if not role:
        raise http_exceptions.ROLE_NOT_FOUND_EXCEPTION

    organization_member = {"user_id": user.id, "organization_id": organization_id, "role_id": role.id}
    created_user = update_organization_member(organization_member)
    current_response = AddOrganizationMemberResponse(
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

