from collections.abc import Iterable
from typing import Any

from .base import SimpleFieldParser


class ListFieldParser(SimpleFieldParser):
    __slots__ = ()

    def parse_value(self, value: Iterable[Any]) -> list[Any]:
        parser = self.args_parsers[0]
        result = (parser.parse_value(item) for item in value)
        try:
            return self.origin(result)
        except Exception:
            return [*result]

    def dump_value(self, value: Iterable[Any]) -> list[Any]:
        parser = self.args_parsers[0]
        return [parser.dump_value(item) for item in value]


class TupleFieldParser(ListFieldParser):
    __slots__ = ()

    def parse_value(self, value: Iterable[Any]) -> tuple:
        return tuple(super().parse_value(value))


class SetFieldParser(ListFieldParser):
    __slots__ = ()

    def parse_value(self, value: Iterable[Any]) -> set:
        return set(super().parse_value(value))
