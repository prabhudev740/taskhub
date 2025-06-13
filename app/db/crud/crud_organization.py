from db.base import get_session
from db.models.organization import OrganizationModel


def get_organization_by_name(org_name: str) -> OrganizationModel | None:
    session = get_session()
    org = session.query(OrganizationModel).where(OrganizationModel.name == org_name).first()
    if not org:
        return None
    return org

def create_organization(org: dict) -> OrganizationModel:
    organization = OrganizationModel(**org)
    session = get_session()
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization
