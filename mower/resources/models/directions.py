from __future__ import annotations
from enum import Enum

from mower.utils.exceptions import OrdinalDirectionError, RelativeDirectionError

class Direction(Enum):
    """Interface for direction types."""

    @classmethod
    def from_str(cls: Direction, d: str) -> Direction:
        """Builds direction from string."""
        pass

    def __str__(self) -> str:
        return f'{self.value}'


class OrdinalDirection(Direction):
    """Ordinal direction model to describe absolute directions."""
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'

    @classmethod
    def from_str(cls: OrdinalDirection, d: str) -> OrdinalDirection:
        """Builds ordinal direction from string."""
        if d == 'N':
            return cls.NORTH
        elif d == 'S':
            return cls.SOUTH
        elif d == 'W':
            return cls.WEST
        elif d == 'E':
            return cls.EAST
        else:
            raise OrdinalDirectionError(value=d, message='Wrong cardinal direction.')


class RelativeDirection(Direction):
    """Relative direction model to describe relative directions."""
    FRONT = 'F'
    BACK = 'B'
    LEFT = 'L'
    RIGHT = 'R'

    @classmethod
    def from_str(cls: RelativeDirection, d: str) -> RelativeDirection:
        """Builds ordinal direction from string."""
        if d == 'F':
            return cls.FRONT
        elif d == 'B':
            return cls.BACK
        elif d == 'L':
            return cls.LEFT
        elif d == 'R':
            return cls.RIGHT
        else:
            raise RelativeDirectionError(value=d, message='Wrong cardinal direction.')
