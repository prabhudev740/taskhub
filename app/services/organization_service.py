from uuid import UUID

from fastapi import HTTPException, status
from db.crud.crud_organization import get_organization_by_name, create_organization
from schemas.organization import CreateOrganization, Organization


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
    organization_response = Organization.model_validate(organization)
    return organization_response
