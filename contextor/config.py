from typing import TypeVar, overload
from pathlib import Path
import asyncio
import io

from typing_extensions import Self
from pydantic import BaseModel, Extra, Field
from ruamel.yaml import YAML


config: "Config"
T = TypeVar("T")
yaml = YAML(typ="safe", pure=True)
loop = asyncio.get_event_loop_policy().get_event_loop()


class Model(BaseModel):
    __abstract__ = True

    class Config:
        extra = Extra.forbid


class Logging(Model):
    history_length: int = Field(10, gt=0)
    debug_files: bool = Field(False)


class Config(Model):
    logging: Logging = Field(default_factory=Logging)

    @classmethod
    def from_dump(cls, dump: dict | Path | str) -> Self:
        assert isinstance(dump, (dict, str, Path))
        return cls(**cls.read_dump(dump))

    @overload
    @staticmethod
    def read_dump(dump: str | Path) -> dict:
        ...

    @overload
    @staticmethod
    def read_dump(dump: T) -> T:
        ...

    @staticmethod
    def read_dump(dump: T) -> dict | T:
        match dump:
            case Path():
                assert dump.exists() and dump.is_file()
                with open(dump, "r", encoding="UTF8") as file:
                    return yaml.load(file) or dict()
            case str():
                return yaml.load(io.StringIO(dump)) or dict()
            case _:
                return dump


config = Config.from_dump(Path.cwd() / "config.yml")
