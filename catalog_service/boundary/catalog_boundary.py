from datetime import datetime

from pydantic import BaseModel


class CatalogBoundary(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    @classmethod
    def from_entity(cls, catalog_entity: "CatatlogEntity") -> "CatalogBoundary":
        return cls.model_validate(
            {key: value for key, value in vars(catalog_entity).items() if not key.startswith('_')}
        )
