import uuid
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import String, Float, Boolean, DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from dal.dao import Base


class CatalogEntity(Base):
    __tablename__ = 'catalogs'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def update(self, data: Dict[str, Any]):
        for key, value in data.items():
            if key == 'id': continue
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def from_boundary(cls, catalog_boundary: "CatalogBoundary") -> "CatalogEntity":
        entity = cls(
            name=catalog_boundary.name,
            description=catalog_boundary.description,
            price=catalog_boundary.price,
            category=catalog_boundary.category,
            created_at=catalog_boundary.created_at,
            updated_at=catalog_boundary.updated_at,
            is_active=catalog_boundary.is_active
        )
        return entity
