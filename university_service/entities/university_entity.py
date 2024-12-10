import uuid
from datetime import datetime
from typing import List, Any, Dict

from sqlalchemy import String, ARRAY, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from common.database.base import Base


class UniversityEntity(Base):
    __tablename__ = "universities"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()) )
    country: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    web_pages: Mapped[List[str]] = mapped_column(ARRAY(String))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)

    @classmethod
    def from_boundary(cls, university_boundary: "UniversityBoundary") -> "UniversityEntity":
        return cls(
            country=university_boundary.country,
            name=university_boundary.name,
            web_pages=university_boundary.web_pages,
        )

    def update(self, data: Dict[str, Any]) -> None:
        data.pop('id')
        data.pop('created_at')
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)