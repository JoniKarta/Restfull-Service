import uvicorn
from fastapi import FastAPI

from common.database.base import Base
from common.database.repository import engine
from controllers import university_controller

app = FastAPI()

app.include_router(university_controller.router)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
