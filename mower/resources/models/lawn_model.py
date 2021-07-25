from __future__ import annotations
from pydantic import BaseModel

from mower.utils.exceptions import LawnModelLoadError


class LawnModel(BaseModel):
    """Lawn model."""

    height: int
    width: int

    @classmethod
    def from_str(cls: LawnModel, lawn_input: str) -> LawnModel:
        """Build a LawnModel from formatted string."""
        try:
            h, w = lawn_input.split()
            return LawnModel(height=int(h), width=int(w))
        except ValueError:
            raise LawnModelLoadError(value=lawn_input, message='Wrong Lawn params in the input file.')
