from typing import TypeVar, Type

from dataclasses_json import DataClassJsonMixin

from exceptions import ProductBuilderException
from helpers import load_data

T = TypeVar('T')


def _build(cls: Type[T], file_name: str) -> list[T]:
    if not issubclass(cls, DataClassJsonMixin):
        raise ProductBuilderException(f"{cls.__name__} must be a subclass of DataClassJsonMixin")
    obj = load_data(f"{file_name}")
    if isinstance(obj, list):
        return [cls.from_dict(item) for item in obj]
    return [cls.from_dict(obj)]


class ProductBuilder:
    @classmethod
    def build(cls, _cls: Type[T], file_name: str) -> list[T]:
        return _build(_cls, file_name)
