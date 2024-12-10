from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UniversityBoundary(BaseModel):
    id: Optional[str] = ""
    country: str = Field(min_length=1)
    name: str = Field(min_length=1)
    web_pages: List[str]
    created_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, university_entity: "UniversityEntity") -> "UniversityBoundary":
        return cls.model_validate(
            {key: value for key, value in vars(university_entity).items() if not key.startswith('_')})
