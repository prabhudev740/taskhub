from fastapi import APIRouter, Path
from typing import Annotated
from schemas.organization import Organization, CreateOrganization
from services.organization_service import crate_new_organization
from services.user_service import CurrentActiveUserDep

router = APIRouter(prefix="/api/v1", tags=["organizations"])


@router.get("/organization")
async def get_organization():
    ...

@router.post("/organization")
async def create_organization(org: CreateOrganization,
                              current_user: CurrentActiveUserDep) -> Organization:
    org = await crate_new_organization(org, current_user_id=current_user.id)
    organization = Organization.model_validate(org)
    return organization

@router.get("/organization/{org_id}")
async def get_organization_by_id(org_id: Annotated[str, Path(...)]):
    ...

@router.put("/organization/{org_id}")
async def update_organization_by_id(org_id: Annotated[str, Path(...)]):
    ...

@router.delete("/organization/{org_id}")
async def delete_organization_by_id(org_id: Annotated[str, Path(...)]):
    ...

@router.get("/organization/{org_id}/members")
async def add_member_to_organization(org_id: Annotated[str, Path(...)]):
    ...

@router.post("/organization/{org_id}/members")
async def get_organization_members(org_id: Annotated[str, Path(...)]):
    ...
