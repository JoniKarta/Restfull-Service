import json
from asyncio import get_event_loop
from typing import List

import httpx

from boundaries.university_boundary import UniversityBoundary
from dal.dao import create_session
from entities.university_entity import UniversityEntity

URL = 'http://universities.hipolabs.com/search?country=United+States'


async def fetch_universities(url: str = URL) -> List[UniversityBoundary]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        list_data = json.loads(response.text)
        university_boundaries = [UniversityBoundary(**data) for data in list_data]
        return university_boundaries


def load_data():
    session = next(create_session())
    loop = get_event_loop()
    university_boundaries = loop.run_until_complete(fetch_universities())
    for university in university_boundaries:
        entity = UniversityEntity.from_boundary(university)
        session.add(entity)
        session.commit()
        session.refresh(entity)
