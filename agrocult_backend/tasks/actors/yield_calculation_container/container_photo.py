import logging
from datetime import datetime
from random import randint

from tortoise import Tortoise

from agrocult_backend.db.config import TORTOISE_CONFIG
from agrocult_backend.db.models.yield_calculation_container_photo import (
    YieldCalculationContainerPhoto,
    YieldCalculationContainerPhotoStatus,
)

logger = logging.getLogger("actors.process_container_photos")


async def process_container_photo(photo_id: int):
    await Tortoise.init(config=TORTOISE_CONFIG)
    await Tortoise.generate_schemas()

    photo = await YieldCalculationContainerPhoto.get(pk=photo_id)

    if not photo or photo.status != YieldCalculationContainerPhotoStatus.processing:
        return None

    logger.info(
        "Containers #%s photo #%s processing!!!",
        (await photo.container).pk,
        photo.pk,
    )

    photo.average_grains_in_basket = randint(350, 850)  # FIXME: add ai magic
    photo.status = YieldCalculationContainerPhotoStatus.complete
    photo.calculated_at = datetime.now()

    await photo.save()

    await Tortoise.close_connections()
