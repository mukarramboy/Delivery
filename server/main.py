from fastapi import FastAPI
from api.routers import aunteficate
from schemas.user_schema import Settings
from fastapi_jwt_auth2 import AuthJWT


app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.openapi_schema = None
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Добавляем схему безопасности ко всем эндпоинтам
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


app.include_router(aunteficate.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}