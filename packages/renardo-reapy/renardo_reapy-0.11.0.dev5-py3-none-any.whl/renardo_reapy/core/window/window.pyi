import renardo_reapy.runtime as runtime
from renardo_reapy.core import ReapyObject
import renardo_reapy.reascript_api as RPR
import typing as ty


class Window(ReapyObject):
    id: bytes

    def __init__(self, id: bytes) -> None:
        ...

    @property
    def _args(self) -> ty.Tuple[bytes]:
        ...

    def refresh(self) -> None:
        """Refresh window."""
        ...
