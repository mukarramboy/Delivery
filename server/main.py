from fastapi import FastAPI
from api.routers import aunteficate
from fastapi_jwt_auth import AuthJWT
from schemas.user_schema import Settings


app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(aunteficate.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}