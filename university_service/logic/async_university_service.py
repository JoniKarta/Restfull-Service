from asyncio import get_event_loop
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from boundaries.pagination import Pagination
from boundaries.university_boundary import UniversityBoundary
from entities.university_entity import UniversityEntity
from logic.university_service import UniversityService


class AsyncUniversityService(UniversityService):

    def __init__(self, university_dao: Optional[Session] = None):
        self._university_dao: Optional[Session] = university_dao

    def set_university_dao(self, university_dao: Session):
        self._university_dao = university_dao

    @classmethod
    def _run_query_in_executor(cls, func):
        loop = get_event_loop()
        return loop.run_in_executor(None, func)

    async def get_universities(self, pagination: Pagination) -> List[UniversityBoundary]:
        if not self._university_dao:
            raise ValueError("University DAO is not set")

        def query_get_universities():
            order_by = desc(pagination.order_by) if pagination.desc else asc(pagination.order_by)
            query_response = (self._university_dao.query(UniversityEntity)
                              .order_by(order_by)
                              .offset(pagination.offset())
                              .limit(pagination.size)
                              .all())
            university_boundaries = [UniversityBoundary.from_entity(entity) for entity in query_response]
            return university_boundaries

        return await self._run_query_in_executor(query_get_universities)

    async def get_university_by_id(self, university_id: str) -> Optional[UniversityBoundary]:
        if not self._university_dao:
            raise ValueError("University DAO is not set")

        def query_get_university_by_id():
            return self._university_dao.query(UniversityEntity).where(
                UniversityEntity.id == university_id).one_or_none()

        result = await self._run_query_in_executor(query_get_university_by_id)
        return UniversityBoundary.from_entity(result) if result else None

    async def create_university(self, university: UniversityBoundary) -> UniversityBoundary:
        if not self._university_dao:
            raise ValueError("University DAO is not set")

        def query_create_university():
            entity = UniversityEntity.from_boundary(university)
            self._university_dao.add(entity)
            self._university_dao.commit()
            self._university_dao.refresh(entity)
            return UniversityBoundary.from_entity(entity)

        return await self._run_query_in_executor(query_create_university)

    async def update_university(self, university_id: str, update: UniversityBoundary) -> Optional[UniversityBoundary]:
        if not self._university_dao:
            raise ValueError("University DAO is not set")

        def query_update_university():
            entity = self._university_dao.query(UniversityEntity).where(
                UniversityEntity.id == university_id).one_or_none()
            if not entity:
                return None
            entity.update(data=update.model_dump())  # Assuming update model contains the new data
            self._university_dao.add(entity)
            self._university_dao.commit()
            self._university_dao.refresh(entity)
            return UniversityBoundary.from_entity(entity)

        return await self._run_query_in_executor(query_update_university)

    async def delete_university(self, university_id: str) -> bool:
        if not self._university_dao:
            raise ValueError("University DAO is not set")

        def query_delete_university():
            if not university_id:
                return False
            entity = self._university_dao.query(UniversityEntity).where(
                UniversityEntity.id == university_id).one_or_none()
            if not entity:
                return False
            self._university_dao.delete(entity)
            self._university_dao.commit()
            return True

        return await self._run_query_in_executor(query_delete_university)
