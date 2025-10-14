from fastapi import FastAPI
from api.routers import aunteficate


app = FastAPI()

app.include_router(aunteficate.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}