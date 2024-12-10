from abc import ABC, abstractmethod
from typing import List, Optional

from boundaries.pagination import Pagination
from boundaries.university_boundary import UniversityBoundary


class UniversityService(ABC):

    @abstractmethod
    async def get_universities(self, pagination: Pagination) -> List[UniversityBoundary]:
        ...

    @abstractmethod
    async def get_university_by_id(self, university_id: str) -> Optional[UniversityBoundary]:
        ...

    @abstractmethod
    async def create_university(self, university: UniversityBoundary) -> UniversityBoundary:
        ...

    @abstractmethod
    async def update_university(self, university_id: str, update: UniversityBoundary) -> Optional[UniversityBoundary]:
        ...

    @abstractmethod
    async def delete_university(self, university_id: str) -> None:
        ...
