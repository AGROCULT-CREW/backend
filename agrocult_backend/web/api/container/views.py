import asyncio
from http import HTTPStatus
from typing import List
from uuid import uuid4

import orjson
from fastapi import APIRouter, File, HTTPException, Path, UploadFile
from starlette.websockets import WebSocket

from agrocult_backend.db.models.grain_culture import GrainCulture
from agrocult_backend.db.models.yield_calculation_container import (
    YieldCalculationContainer,
    YieldCalculationContainerStatus,
)
from agrocult_backend.db.models.yield_calculation_container_photo import (
    YieldCalculationContainerPhoto,
)
from agrocult_backend.services.s3.storage import FileStorage
from agrocult_backend.web.api.container.schema import (
    YieldCalculationContainerCreateRequest,
    YieldCalculationContainerCreateResponse,
    YieldCalculationContainerGetResponse,
    YieldCalculationContainerPhotoGetResponse,
)

router = APIRouter()


@router.get("/", response_model=List[YieldCalculationContainerGetResponse])
async def get_containers_list() -> List[YieldCalculationContainerGetResponse]:
    response = []

    async for container in YieldCalculationContainer.all().order_by("-created_at"):
        container.average_weight_thousand_grains = await (
            container.get_average_weight_thousand_grains()
        )
        container.average_stems_per_meter = (
            await container.get_average_stems_per_meter() or None
        )

        if not await container.grain_culture:
            container.grain_culture = None

        else:
            container.grain_culture_id = (await container.grain_culture).pk

        response.append(
            await YieldCalculationContainerGetResponse.from_tortoise_orm(
                container,
            ),
        )

    return response


@router.post("/", response_model=YieldCalculationContainerCreateResponse)
async def create_container(
    schema: YieldCalculationContainerCreateRequest,
) -> YieldCalculationContainerCreateResponse:
    create_schema = schema.dict()

    if schema.grain_culture_id:
        if grain_culture := await GrainCulture.get_or_none(
            pk=schema.grain_culture_id,
        ):
            create_schema["grain_culture"] = grain_culture
        else:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Grain culture not found!")

    new_container = YieldCalculationContainer(**create_schema)
    await new_container.save()

    new_container.average_weight_thousand_grains = await (
        new_container.get_average_weight_thousand_grains()
    )
    new_container.average_stems_per_meter = (
        await new_container.get_average_stems_per_meter() or None
    )

    new_container.grain_culture_id = (
        None if not new_container.grain_culture else new_container.grain_culture.pk
    )

    response = await YieldCalculationContainerCreateResponse.from_tortoise_orm(
        new_container,
    )

    return response


@router.websocket("/{container_id}/results/")
async def get_container_results(websocket: WebSocket, container_id: int = Path(...)):
    await websocket.accept()

    while True:
        await asyncio.sleep(1)

        if container := await YieldCalculationContainer.get_or_none(
            pk=container_id,
        ):
            if container.status not in (
                YieldCalculationContainerStatus.processing,
                YieldCalculationContainerStatus.internal_error,
                YieldCalculationContainerStatus.complete,
            ):
                await websocket.send_json(
                    {
                        "code": HTTPStatus.BAD_REQUEST,
                        "message": "Container on created stage!",
                    },
                )
                break

            if container.status == YieldCalculationContainerStatus.processing:
                await websocket.send_json({"status": str(container.status)})

            elif container.status == YieldCalculationContainerStatus.internal_error:
                await websocket.send_json(
                    {
                        "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "message": "Container processing error!",
                    },
                )
                break

            else:
                container.average_weight_thousand_grains = await (
                    container.get_average_weight_thousand_grains()
                )
                container.average_stems_per_meter = (
                    await container.get_average_stems_per_meter() or None
                )

                if not await container.grain_culture:
                    container.grain_culture = None

                else:
                    container.grain_culture_id = (await container.grain_culture).pk

                response = await YieldCalculationContainerGetResponse.from_tortoise_orm(
                    container,
                )

                response = orjson.dumps(response.dict())

                await websocket.send({"type": "websocket.send", "bytes": response})
                break
        else:
            await websocket.send_json(
                {"code": HTTPStatus.NOT_FOUND, "message": "Container not found!"},
            )
            break

    await websocket.close()


@router.get(
    "/{container_id}/files/",
    response_model=List[YieldCalculationContainerPhotoGetResponse],
)
async def get_container_files(
    container_id: int = Path(...),
) -> List[YieldCalculationContainerPhotoGetResponse]:
    if container := await YieldCalculationContainer.get_or_none(
        pk=container_id,
    ):
        response = []

        async for photo in container.photos.all():
            photo.container_id = container_id

            response.append(
                await YieldCalculationContainerPhotoGetResponse.from_tortoise_orm(
                    photo,
                ),
            )
    else:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Container not found!")

    return response


@router.post(
    "/{container_id}/files/",
    response_model=List[YieldCalculationContainerPhotoGetResponse],
)
async def upload_container_photo(
    container_id: int = Path(...),
    file: UploadFile = File(...),
) -> List[YieldCalculationContainerPhotoGetResponse]:
    if container := await YieldCalculationContainer.get_or_none(
        pk=container_id,
    ):
        new_photo = YieldCalculationContainerPhoto()

        new_photo.file_name = file.filename
        new_photo.unique_file_name = f"{uuid4()}_{file.filename}"
        new_photo.container = container
        new_photo.s3_path = await FileStorage.upload_file(
            body=file.file.read(),
            file_name=new_photo.unique_file_name,
            prefix=f"containers/photos/{container.pk}",
        )

        await new_photo.save()

        response = []

        async for photo in container.photos.all():
            photo.container_id = container_id

            response.append(
                await YieldCalculationContainerPhotoGetResponse.from_tortoise_orm(
                    photo,
                ),
            )
    else:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Container not found!")

    return response


@router.post("/{container_id}/start/", response_model=bool)
async def start_container_processing(
    container_id: int = Path(...),
) -> bool:
    if container := await YieldCalculationContainer.get_or_none(
        pk=container_id,
    ):
        if not await container.photos.all():
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Photos not found!")

        container.status = YieldCalculationContainerStatus.processing

        await container.save()
    else:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Container not found!")

    return True


@router.get("/{container_id}/", response_model=YieldCalculationContainerGetResponse)
async def get_container(
    container_id: int = Path(...),
) -> YieldCalculationContainerGetResponse:
    if container := await YieldCalculationContainer.get_or_none(
        pk=container_id,
    ):
        container.average_weight_thousand_grains = await (
            container.get_average_weight_thousand_grains()
        )
        container.average_stems_per_meter = (
            await container.get_average_stems_per_meter() or None
        )

        if not await container.grain_culture:
            container.grain_culture = None

        else:
            container.grain_culture_id = (await container.grain_culture).pk

        response = await YieldCalculationContainerGetResponse.from_tortoise_orm(
            container,
        )
    else:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Container not found!")

    return response


@router.get("/{container_id}/kml")
async def get_container_kml(
    container_id: int = Path(...),
):
    if container := await YieldCalculationContainer.get_or_none(
        pk=container_id,
    ):
        if container.status != YieldCalculationContainerStatus.complete:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                f"Bad status - {container.status}!",
            )

    else:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Container not found!")
