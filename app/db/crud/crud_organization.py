from db.base import get_session
from db.models.organization import OrganizationModel, OrganizationMemberModel
from uuid import UUID


def get_organizations_by_member_id(user_id: UUID, page: int, size: int,
                             sort_by: str = "joined_at") -> tuple[list[OrganizationModel], int, int]:
    session = get_session()
    items = (session.query(OrganizationModel)
            # .join(OrganizationMemberModel, OrganizationMemberModel.user_id == OrganizationModel.id)
            .join(OrganizationMemberModel, OrganizationMemberModel.organization_id == OrganizationModel.id)
            .filter(OrganizationMemberModel.user_id == user_id)
    )
    sorted_items = items.order_by(getattr(OrganizationMemberModel, sort_by))
    total = sorted_items.count()
    response_items = sorted_items.offset((page - 1) * size).limit(size).all()
    pages = (total + size - 1) // size
    return response_items, total, pages

def get_organization_by_name(org_name: str):
    session = get_session()
    organization = session.query(OrganizationModel).filter_by(name=org_name).first()
    if not organization:
        return None
    return organization

def get_organization_by_id(organization_id: UUID):
    session = get_session()
    organization = session.query(OrganizationModel).filter_by(id=organization_id).first()
    if not organization:
        return None
    return organization

def create_organization(org: dict) -> OrganizationModel:
    organization = OrganizationModel(**org)
    session = get_session()
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization

def update_organization_member(organization_member_datar: dict) -> OrganizationMemberModel:
    organization_member = OrganizationMemberModel(**organization_member_datar)
    session = get_session()
    session.add(organization_member)
    session.commit()
    session.refresh(organization_member)
    return organization_member

# def get_organization_members(organization_id: UUID, user_id: UUID) -> OrganizationMemberModel:
#     session = get_session()
#     organization_members = session.query(OrganizationMemberModel).filter_by()
#     if not organization_members:
#         return None
#     return organization_member

def get_organization_member_by_organization_user_id(org_id: UUID, user_id: UUID) -> OrganizationMemberModel | None:
    session = get_session()
    organization_member = \
        session.query(OrganizationMemberModel).filter_by(user_id=user_id, organization_id=org_id).first()
    if not organization_member:
        return None
    return organization_member

def get_organization_member_by_organization_id(org_id: UUID) -> int:
    session = get_session()
    count = session.query(OrganizationMemberModel).filter_by(organization_id=org_id).count()
    return count