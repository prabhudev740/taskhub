from uuid import UUID
from fastapi import HTTPException, status
from db.crud.crud_organization import get_organization_by_name, create_organization, add_organization_member, \
    get_organizations_by_member_id
from db.crud.crud_user import get_user_by_id
from db.crud.curd_role import get_role_by_name, create_role
from schemas.organization import CreateOrganization, Organization, OrganizationResponse, OrganizationUserRole, \
    AddOrganizationMembersRequest, AddOrganizationMemberResponse


async def get_role_id(role_name):
    role = get_role_by_name(role_name)
    if not role:
        role = create_role(role_name=role_name)
    return role.id

async def crate_new_organization(org: CreateOrganization, current_user_id: UUID) -> Organization:
    org_exists_conflict = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Organization with same name already exists."
    )
    if get_organization_by_name(org.name):
        raise org_exists_conflict
    organization_data = org.model_dump(exclude_unset=True)
    organization_data.update({"owner_id": current_user_id})
    organization = create_organization(organization_data)

    role_id = await get_role_id("owner")
    organization_member = {"user_id": current_user_id, "organization_id": organization.id, "role_id": role_id}
    add_organization_member(organization_member)
    return Organization.model_validate(organization)


async def get_organization_details(user_id: UUID, page: int, size: int, sort_by: str) -> OrganizationResponse:
    items, total, pages = get_organizations_by_member_id(user_id=user_id, page=page, size=size, sort_by=sort_by)
    organizations = list(map(Organization.model_validate, items))
    organizations_response = OrganizationResponse(items=organizations, total=total, pages=pages, page=page, size=size)
    return organizations_response


async def add_new_members_to_organization(user_roles: AddOrganizationMembersRequest) -> AddOrganizationMemberResponse:
    for user_role in user_roles:
        # user_role.username
        # user_role.role
        ...

    return AddOrganizationMemberResponse.model_validate(...)


async def verify_current_user_role(user_id: UUID, org_id: UUID, permission: str):
    user = get_user_by_id(user_id=user_id)

    ...
