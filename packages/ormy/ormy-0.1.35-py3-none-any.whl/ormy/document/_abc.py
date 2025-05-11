from abc import abstractmethod
from typing import Any, ClassVar, Mapping, Self, TypeVar, cast

from pydantic import Field

from ormy._abc import (
    AbstractABC,
    AbstractMixinABC,
    ConfigABC,
    SemiFrozenField,
)
from ormy.base.func import hex_uuid4
from ormy.base.pydantic import IGNORE
from ormy.base.typing import AbstractData
from ormy.exceptions import Conflict

# ----------------------- #

C = TypeVar("C", bound=ConfigABC)

# TODO: DocumentConfigABC ???

# ....................... #


class BaseDocumentABC(AbstractABC):
    """Abstract Base Class for Document-Oriented ORM"""

    id: str = Field(default_factory=hex_uuid4)

    semi_frozen_fields: ClassVar[Mapping[str, SemiFrozenField | dict[str, Any]]] = {}
    __discriminator__: ClassVar[list[str]] = []

    # ....................... #

    def __init_subclass__(cls, **kwargs):
        """Initialize subclass"""

        super().__init_subclass__(**kwargs)
        cls.__parse_semi_frozen_fields()

    # ....................... #

    @classmethod
    def __parse_semi_frozen_fields(cls):
        """Parse semi-frozen fields"""

        new = {}

        for field, value in cls.semi_frozen_fields.items():
            if isinstance(value, dict):
                new[field] = SemiFrozenField(**value)

            else:
                new[field] = value

        cls.semi_frozen_fields = new


# ....................... #


class SyncDocumentABC(BaseDocumentABC):
    """Abstract Base Class for Document-Oriented ORM (Sync)"""

    @classmethod
    @abstractmethod
    def create(cls, data: Self) -> Self: ...

    # ....................... #

    @abstractmethod
    def save(self: Self) -> Self: ...

    # ....................... #

    @classmethod
    @abstractmethod
    def find(cls, id_: str) -> Self: ...

    # ....................... #

    @abstractmethod
    def kill(self: Self) -> None: ...

    # ....................... #

    @classmethod
    @abstractmethod
    def kill_many(cls, *args: Any, **kwargs: Any) -> None: ...

    # ....................... #

    def update(
        self: Self,
        data: AbstractData,
        autosave: bool = True,
        soft_frozen: bool = True,
    ):
        """
        Update the document with the given data

        Args:
            data (AbstractData): Data to update the document with
            autosave (bool): Save the document after updating
            soft_frozen (bool): Whether to allow soft frozen fields to be updated

        Returns:
            self (Self): Updated document
        """

        if isinstance(data, dict):
            keys = data.keys()

        else:
            keys = data.model_fields.keys()
            data = data.model_dump()

        for k in keys:
            val = data.get(k, IGNORE)

            if val != IGNORE and k in self.model_fields:
                if k in self.semi_frozen_fields.keys():
                    _semi = self.semi_frozen_fields[k]
                    semi = cast(SemiFrozenField, _semi)

                    if semi.evaluate(self):
                        if not soft_frozen:
                            raise Conflict(
                                f"Field {k} is semi-frozen within context {semi.context}"
                            )

                        else:
                            continue

                elif self.model_fields[k].frozen:
                    if not soft_frozen:
                        raise Conflict(f"Field {k} is frozen")

                    else:
                        continue

                setattr(self, k, val)

        if autosave:
            return self.save()

        return self


# ....................... #


class AsyncDocumentABC(BaseDocumentABC):
    """Abstract Base Class for Document-Oriented ORM (Async)"""

    @classmethod
    @abstractmethod
    async def acreate(cls, data: Self) -> Self: ...

    # ....................... #

    @abstractmethod
    async def asave(self: Self) -> Self: ...

    # ....................... #

    @classmethod
    @abstractmethod
    async def afind(cls, id_: str) -> Self: ...

    # ....................... #

    @abstractmethod
    async def akill(self: Self) -> None: ...

    # ....................... #

    @classmethod
    @abstractmethod
    async def akill_many(cls, *args: Any, **kwargs: Any) -> None: ...

    # ....................... #

    async def aupdate(
        self: Self,
        data: AbstractData,
        autosave: bool = True,
        soft_frozen: bool = True,
    ):
        """
        Update the document with the given data

        Args:
            data (AbstractData): Data to update the document with
            autosave (bool): Save the document after updating
            soft_frozen (bool): Whether to allow soft frozen fields to be updated

        Returns:
            self (Self): Updated document
        """

        if isinstance(data, dict):
            keys = data.keys()

        else:
            keys = data.model_fields.keys()
            data = data.model_dump()

        for k in keys:
            val = data.get(k, IGNORE)

            if val != IGNORE and k in self.model_fields:
                if k in self.semi_frozen_fields.keys():
                    _semi = self.semi_frozen_fields[k]
                    semi = cast(SemiFrozenField, _semi)

                    if semi.evaluate(self):
                        if not soft_frozen:
                            raise Conflict(
                                f"Field {k} is semi-frozen within context {semi.context}"
                            )

                        else:
                            continue

                elif self.model_fields[k].frozen:
                    if not soft_frozen:
                        raise Conflict(f"Field {k} is frozen")

                    else:
                        continue

                setattr(self, k, val)

        if autosave:
            return await self.asave()

        return self


# ....................... #


class DocumentABC(SyncDocumentABC, AsyncDocumentABC):
    """Document ABC Base Class with sync and async methods"""


# ....................... #


class DocumentMixinABC(AbstractMixinABC):
    """Document Mixin ABC Base Class"""
