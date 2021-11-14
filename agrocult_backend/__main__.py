import uvicorn

from agrocult_backend.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "agrocult_backend.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
        reload_dirs=["./agrocult_backend/"],
    )


if __name__ == "__main__":
    main()
