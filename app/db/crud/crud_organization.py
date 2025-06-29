""" Org CRUD """

from uuid import UUID
from db.base import get_session
from db.models.organization import OrganizationModel, OrganizationMemberModel


def get_organizations_by_member_id(user_id: UUID, page: int, size: int,
                                   sort_by: str = "joined_at"
                                   ) -> tuple[list[OrganizationModel], int, int]:
    """
    Retrieve organizations associated with a specific member ID.

    Args:
        user_id (UUID): The ID of the user whose organizations are being retrieved.
        page (int): The page number for pagination.
        size (int): The number of items per page.
        sort_by (str): The field to sort the organizations by (default is "joined_at").

    Returns:
        tuple: A tuple containing:
            - list[OrganizationModel]: List of organizations.
            - int: Total number of organizations.
            - int: Total number of pages.
    """
    session = get_session()
    items = (session.query(OrganizationModel)
            .join(
        OrganizationMemberModel, OrganizationMemberModel.organization_id == OrganizationModel.id)
             .filter(OrganizationMemberModel.user_id == user_id)
             )
    sorted_items = items.order_by(getattr(OrganizationMemberModel, sort_by))
    total = sorted_items.count()
    response_items = sorted_items.offset((page - 1) * size).limit(size).all()
    pages = (total + size - 1) // size
    return response_items, total, pages

def get_organization_by_name(org_name: str):
    """
    Retrieve an organization by its name.

    Args:
        org_name (str): The name of the organization.

    Returns:
        OrganizationModel | None: The organization if found, otherwise None.
    """
    session = get_session()
    organization = session.query(OrganizationModel).filter_by(name=org_name).first()
    if not organization:
        return None
    return organization

def get_organization_by_id(organization_id: UUID):
    """
    Retrieve an organization by its ID.

    Args:
        organization_id (UUID): The ID of the organization.

    Returns:
        OrganizationModel | None: The organization if found, otherwise None.
    """
    session = get_session()
    organization = session.query(OrganizationModel).filter_by(id=organization_id).first()
    if not organization:
        return None
    return organization

def create_organization(org: dict) -> OrganizationModel:
    """
    Create a new organization.

    Args:
        org (dict): A dictionary containing organization details.

    Returns:
        OrganizationModel: The newly created organization.
    """
    organization = OrganizationModel(**org)
    session = get_session()
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization

def update_organization(organization_id: UUID, org: dict) -> type[OrganizationModel] | None:
    """
    Update an organization's details.

    Args:
        organization_id (UUID): The ID of the organization to update.
        org (dict): A dictionary containing updated organization details.

    Returns:
        OrganizationModel | None: The updated organization if found, otherwise None.
    """
    session = get_session()
    organization = session.query(OrganizationModel).filter_by(id=organization_id).first()
    if not organization:
        return None

    for key, val in org.items():
        setattr(organization, key, val)
    session.commit()
    session.refresh(organization)
    return organization

def delete_organizations_by_id(organization_id: UUID) -> bool:
    """
    Delete an organization by its ID.

    Args:
        organization_id (UUID): The ID of the organization to delete.

    Returns:
        bool: True if the organization was deleted, False otherwise.
    """
    session = get_session()
    organization = session.query(OrganizationModel).filter_by(id=organization_id).first()
    if not organization:
        return False
    session.query(OrganizationMemberModel).filter_by(organization_id=organization_id).delete()
    session.delete(organization)
    session.commit()
    return True

def update_organization_member(organization_member_datar: dict) -> OrganizationMemberModel:
    """
    Update an organization member's details.

    Args:
        organization_member_datar (dict): A dictionary containing updated member details.

    Returns:
        OrganizationMemberModel: The updated organization member.
    """
    organization_member = OrganizationMemberModel(**organization_member_datar)
    session = get_session()
    session.add(organization_member)
    session.commit()
    session.refresh(organization_member)
    return organization_member

def get_organization_members_by_organization_id(organization_id: UUID,
                                                page: int, size: int, sort_by: str
                                                ) -> tuple[list[
                                                    type[OrganizationMemberModel]], int, int]:
    """
    Retrieve members of an organization by id.

    Args:
        organization_id (UUID): The ID of the organization.
        page (int): The page number for pagination.
        size (int): The number of items per page.
        sort_by (str): The field to sort the organizations by (default is "joined_at").

    Returns:
        tuple: A tuple containing:
            - list[OrganizationMemberModel]: List of organizations.
            - int: Total number of organizations.
            - int: Total number of pages.
    """
    session = get_session()
    items = session.query(OrganizationMemberModel).filter_by(organization_id=organization_id)
    sorted_members = items.order_by(getattr(OrganizationMemberModel, sort_by))
    total = sorted_members.count()
    response_items = sorted_members.offset((page - 1) * size).limit(size).all()
    pages = (total + size - 1) // size
    return response_items, total, pages

def get_organization_member_by_organization_user_id(org_id: UUID, user_id: UUID
                                                    ) -> type[OrganizationMemberModel] | None:
    """
    Retrieve an organization member by organization ID and user ID.

    Args:
        org_id (UUID): The ID of the organization.
        user_id (UUID): The ID of the user.

    Returns:
        OrganizationMemberModel | None: The organization member if found, otherwise None.
    """
    session = get_session()
    organization_member = \
        session.query(OrganizationMemberModel).filter_by(
            user_id=user_id, organization_id=org_id).first()
    if not organization_member:
        return None
    return organization_member

def get_organization_member_count_by_organization_id(org_id: UUID) -> int:
    """
    Count the number of members in an organization.

    Args:
        org_id (UUID): The ID of the organization.

    Returns:
        int: The number of members in the organization.
    """
    session = get_session()
    count = session.query(OrganizationMemberModel).filter_by(organization_id=org_id).count()
    return count

def update_organization_member_role(org_id: UUID, user_id: UUID, role_id: UUID
                                    ) -> type[OrganizationMemberModel] | None:
    """
    Update the role in the organization by organization ID and member ID

    Args:
        org_id (UUID): The ID of the organization.
        user_id (UUID): The ID of user in the organization.
        role_id (UUID): The ID new role.

    Returns:
        OrganizationMemberModel | None: The organization member if found, otherwise None.
    """
    session = get_session()
    member = session.query(OrganizationMemberModel).filter_by(
        organization_id=org_id, user_id=user_id).first()
    if not member:
        return None
    setattr(member, "role_id", role_id)
    session.commit()
    session.refresh(member)
    return member
