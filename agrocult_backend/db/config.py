from typing import List

from agrocult_backend.settings import settings

MODELS_MODULES: List[str] = [
    "agrocult_backend.db.models.grain_culture",
    "agrocult_backend.db.models.yield_calculation_container",
    "agrocult_backend.db.models.yield_calculation_container_photo",
]

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": ["aerich.models"] + MODELS_MODULES,
            "default_connection": "default",
        },
    },
}
