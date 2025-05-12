from collections.abc import Mapping
from typing import Any, Self

from .types import Attr, Index, Key, NonStrSequence, TypeContainer
from .utils import ArgsProcessor


class PullOut:
    """
    Извлечение данных из объекта с помощью цепочки атрибутов, индексов и ключей.
    См. README в папке с кодом класса.
    """

    default: Any | None = None

    def __init__(self, *args, default: Any | None = None) -> None:
        self.args = ArgsProcessor(*args).prepare()
        self.default = default

    def From(self, object_from, default: Any | None = None) -> Any:  # noqa: N802 (Ruff)
        """
        Извлечение указанных при инициализации данных из переданного объекта.
        """
        if default is not None:
            self.default = default
        self.obj = object_from
        return self._extract_args()

    def __call__(self, object_from, default: Any | None = None) -> Any:
        """
        Извлечение указанных при инициализации данных из переданного объекта.
        """
        return self.From(object_from, default)

    def use_default(self, default: Any) -> Self:
        """
        Установка нового значения по умолчанию для извлечения данных.
        """
        self.default = default
        return self

    def _extract_next(self, what_to_extract: Any, from_where: Any) -> Any:
        if isinstance(what_to_extract, TypeContainer):
            return what_to_extract(from_where) or self.default
        if isinstance(from_where, Mapping):
            return Key(what_to_extract)(from_where) or self.default
        if isinstance(from_where, NonStrSequence):
            return Index(what_to_extract)(from_where)
        return Attr(what_to_extract)(from_where) or self.default

    def _extract_args(self) -> Any | None:
        _obj = self.obj
        for arg in self.args:
            try:
                _obj = self._extract_next(arg, _obj)
            except (ValueError, TypeError, KeyError):
                return self.default
            if _obj is None:
                break
        return _obj or self.default
