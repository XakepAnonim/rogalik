"""
Модуль содержит функции для работы с JSON-данными.
"""

import contextlib
import json
from collections.abc import Iterable
from json import JSONDecodeError

from fastapi.encoders import jsonable_encoder
from pydantic_core._pydantic_core import PydanticSerializationError

from models.base import json_


def to_json(data: dict) -> json_:
    """
    Преобразует данные в формат JSON.
    """
    try:
        return json.dumps(data)
    except (TypeError, PydanticSerializationError):
        correct_data = jsonable_encoder(data)
        return json.dumps(correct_data)


def from_json(data: json_) -> dict | str:
    """
    Преобразует данные из формата JSON.
    """
    if isinstance(data, json_):
        with contextlib.suppress(JSONDecodeError):
            data = json.loads(data)
    if not isinstance(data, Iterable) or isinstance(data, str):
        return data

    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = from_json(value)
    elif isinstance(data, Iterable):
        for i, value in enumerate(data):
            data[i] = from_json(value)

    return data
