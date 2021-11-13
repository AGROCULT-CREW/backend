from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from agrocult_backend.db.config import TORTOISE_CONFIG
from agrocult_backend.web.api.router import api_router
from agrocult_backend.web.lifetime import shutdown, startup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="agrocult_backend",
        description="",
        version=metadata.version("agrocult_backend"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    app.include_router(router=api_router, prefix="/api")
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )

    return app
