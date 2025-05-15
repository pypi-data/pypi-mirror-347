import asyncio
from collections.abc import Iterable
from typing import Any

from .base import SimpleFieldParser


class ListFieldParser(SimpleFieldParser):
    __slots__ = ()

    async def parse_value(self, value: Iterable[Any]) -> list[Any]:
        parser = self.args_parsers[0]
        result = await asyncio.gather(*[parser.parse_value(item) for item in value])
        try:
            return self.origin(result)
        except Exception:
            return [*result]

    async def dump_value(self, value: Iterable[Any]) -> list[Any]:
        parser = self.args_parsers[0]
        return await asyncio.gather(*[parser.dump_value(item) for item in value])


class TupleFieldParser(ListFieldParser):
    __slots__ = ()

    async def parse_value(self, value: Iterable[Any]) -> tuple:
        return tuple(await super().parse_value(value))


class SetFieldParser(ListFieldParser):
    __slots__ = ()

    async def parse_value(self, value: Iterable[Any]) -> set:
        return set(await super().parse_value(value))
