import uvicorn
from fastapi import FastAPI
from controller import catalog_controller
from dal.dao import Base, engine

app = FastAPI()

app.include_router(catalog_controller.router)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)