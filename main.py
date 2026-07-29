from fastapi import FastAPI

from app.database.database import engine
from app.models.base import Base
from app.models.log_model import Log

from app.routes.log_routes import router

from app.routes import chart_routes


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.include_router(chart_routes.router)


@app.get("/")
def home():

    return {
        "message":"Smart Log Analysis System Running Successfully"
    }