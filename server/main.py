from fastapi import FastAPI
from api.routers import aunteficate
from database.models import User




app = FastAPI()

app.include_router(aunteficate.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}