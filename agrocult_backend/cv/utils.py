import io

import torch
from PIL.Image import Image

from agrocult_backend.settings import settings


def load_model():
    return torch.hub.load(
        "ultralytics/yolov5",
        "custom",
        path=settings.model_path,
        force_reload=True,
    )


model = load_model()


def get_prediction(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    img = img.resize((640, 640))
    img = img.convert("L")
    # inference
    results = model(img, size=640)
    return results
