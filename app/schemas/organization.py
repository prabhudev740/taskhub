from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID
from datetime import datetime

from services.user_service import CurrentActiveUserDep


class Organization(BaseModel):
    id: UUID
    name: str
    description: str
    owner_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CreateOrganization(BaseModel):
    name: Annotated[str,  Field(min_length=5, max_length=32)]
    description: Annotated[str | None,  Field(max_length=1024)]


# class Organization(Base):
#     __tablename__ = "organizations"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String, unique=True, nullable=False, index=True)
#     description = Column(Text, nullable=True)
#     owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

