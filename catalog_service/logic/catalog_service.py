import asyncio
from typing import Optional, List

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from boundary.catalog_boundary import CatalogBoundary
from boundary.pagination import Pagination
from entity.catalog_entity import CatalogEntity


class CatalogService:

    def __init__(self):
        self.catalog_dao: Optional[Session] = None

    def set_catalog_dao(self, catalog_dao: Session) -> None:
        self.catalog_dao = catalog_dao

    async def get_catalogs(self, pagination: Pagination) -> List[CatalogBoundary]:
        order_by = desc(pagination.order_by) if pagination.desc else asc(pagination.order_by)
        return [CatalogBoundary.from_entity(catalog_entity) for catalog_entity in
                self.catalog_dao.query(CatalogEntity)
                .order_by(order_by)
                .offset(pagination.offset())
                .limit(pagination.size)
                .all()
                ]

    async def create_catalog(self, catalog_boundary: CatalogBoundary) -> Optional[CatalogBoundary]:
        entity = CatalogEntity.from_boundary(catalog_boundary)
        self.catalog_dao.add(entity)
        self.catalog_dao.commit()
        self.catalog_dao.refresh(entity)
        return CatalogBoundary.from_entity(entity)

    async def update_catalog(self, catalog_id: str, update_catalog: CatalogBoundary) -> Optional[CatalogBoundary]:
        entity: Optional[CatalogEntity] = self.catalog_dao.query(CatalogEntity).where(
            CatalogEntity.id == catalog_id).one_or_none()
        if not entity:
            raise ValueError(f'Could not found catalog with id {catalog_id}')

        entity.update(data=update_catalog.model_dump())

        self.catalog_dao.add(entity)
        self.catalog_dao.commit()
        self.catalog_dao.refresh(entity)
        return CatalogBoundary.from_entity(entity)

    async def delete_catalog(self, catalog_id: str) -> None:
        entity: Optional[CatalogEntity] = self.catalog_dao.query(CatalogEntity).where(
            CatalogEntity.id == catalog_id).one_or_none()
        if not entity:
            raise ValueError(f'Could not found catalog with id {catalog_id}')

        self.catalog_dao.delete(entity)
