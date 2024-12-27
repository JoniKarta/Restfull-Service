from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (HTTP_200_OK,
                              HTTP_204_NO_CONTENT,
                              HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR)

from boundary.catalog_boundary import CatalogBoundary
from boundary.pagination import Pagination
from dal.dao import get_db
from logic.catalog_service import CatalogService
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


def get_catalog_service(dao: Annotated[Session, Depends(get_db)]):
    catalog_service = CatalogService()
    catalog_service.set_catalog_dao(dao)
    return catalog_service


@router.get('/catalogs', status_code=HTTP_200_OK)
async def get_catalogs(pagination: Annotated[Pagination, Depends()], catalog_service: Annotated[CatalogService, Depends(get_catalog_service)]):
    try:
        return await catalog_service.get_catalogs(pagination)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not get catalogs")


@router.post('/catalogs', status_code=HTTP_201_CREATED)
async def create_catalog(catalog: CatalogBoundary,
                         catalog_service: Annotated[CatalogService, Depends(get_catalog_service)]):
    try:
        return await catalog_service.create_catalog(catalog)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create catalog")


@router.put('/catalogs/{catalog_id}', status_code=HTTP_200_OK)
async def update_catalog(catalog_id: str, catalog: CatalogBoundary,
                         catalog_service: Annotated[CatalogService, Depends(get_catalog_service)]):
    try:
        return await catalog_service.update_catalog(catalog_id, catalog)
    except ValueError as err:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(err))
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update catalog")


@router.delete('/catalogs/{catalog_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_catalog(catalog_id: str, catalog_service: Annotated[CatalogService, Depends(get_catalog_service)]):
    try:
        return await catalog_service.delete_catalog(catalog_id)
    except ValueError as err:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(err))
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not process the request")
