from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from boundaries.pagination import Pagination
from boundaries.university_boundary import UniversityBoundary
from dal.dao import create_session
from logic.async_university_service import AsyncUniversityService
from logic.university_service import UniversityService
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

router = APIRouter()


def university_service(session: Annotated[Session, Depends(create_session)]):
    university_service = AsyncUniversityService()
    university_service.set_university_dao(session)
    return university_service


@router.get('/universities')
async def get_universities(pagination: Annotated[Pagination, Query()],
                           university_service: Annotated[UniversityService, Depends(university_service)]):
    return await university_service.get_universities(pagination)


@router.post('/universities', status_code=HTTP_201_CREATED)
async def create_university(university: UniversityBoundary,
                            university_service: Annotated[UniversityService, Depends(university_service)]):
    return await university_service.create_university(university)


@router.get('/universities/{university_id}', response_model=UniversityBoundary, status_code=HTTP_200_OK)
async def get_university_by_id(university_id: str,
                               university_service: Annotated[UniversityService, Depends(university_service)]):
    response = await university_service.get_university_by_id(university_id)
    if not response:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'University with id = {university_id} not found')
    return response


@router.put('/universities', response_model=UniversityBoundary, status_code=HTTP_200_OK)
async def update_university(university_id: str, update_university: UniversityBoundary,
                            university_service: Annotated[UniversityService, Depends(university_service)]):
    response = await university_service.update_university(university_id, update_university)
    if not response:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'University with id = {university_id} not found')
    return response

@router.delete('/universities/{university_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_university(university_id: str,
                            university_service: Annotated[UniversityService, Depends(university_service)]):
    response = await university_service.delete_university(university_id)
    if not response:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'University with id = {university_id} not found')
