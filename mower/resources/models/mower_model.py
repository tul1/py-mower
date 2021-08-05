from __future__ import annotations
from pydantic import BaseModel
from typing import Tuple, List, Optional
from itertools import cycle
from collections import namedtuple

from mower.resources.models.directions import OrdinalDirection, RelativeDirection
from mower.resources.models.lawn_model import LawnDimensions
from mower.resources.models.position_model import Position
from mower.utils.exceptions import MowerModelLoadError, OrdinalDirectionError, MowerModelError


MowerPosition = namedtuple('MowerPosition', ['x', 'y', 'o'])


class MowerModel(BaseModel):
    """Mower model."""

    position: MowerPosition
    directions: Optional[List[RelativeDirection]] = []

    @staticmethod
    def position_from_str(mower_pos_input: str) -> MowerPosition:
        """Build mower position."""
        try:
            h, w, d = mower_pos_input.split()
            return int(h), int(w), OrdinalDirection.from_str(d)
        except (ValueError, OrdinalDirectionError):
            raise MowerModelLoadError(value=mower_pos_input, message='Wrong Mower position params in the input file.')

    @classmethod
    def from_initial_position_str(cls: MowerModel, mower_init_pos_input: str) -> MowerModel:
        """Build mower from initial position formatted string."""
        return MowerModel(position=MowerModel.position_from_str(mower_init_pos_input))

    @classmethod
    def extend_directions_from_str(cls: MowerModel, base_model: MowerModel, relative_directions: str) -> List[RelativeDirection]:
        """Builds mower realative directions list from string."""
        base_directions = base_model.directions
        new_directions = [RelativeDirection.from_str(direction) for direction in relative_directions if direction != ' ']
        new_directions.extend(base_directions)
        return MowerModel(position=base_model.position, directions=new_directions)

    @staticmethod
    def translate_mower_position(mower_position: MowerPosition, distance: int, direction: RelativeDirection, limit: LawnDimensions) -> MowerPosition:
        """Translate mower position."""
        if direction not in (RelativeDirection.FRONT, RelativeDirection.BACK):
            raise MowerModelError(value=direction, message=f'Mower cannot be translate with a {direction} direction.')
        x, y, o = mower_position
        distance = abs(distance) * (1 if direction == RelativeDirection.FRONT else -1)
        if o == OrdinalDirection.NORTH or o == OrdinalDirection.SOUTH:
            distance *= (1 if o == OrdinalDirection.NORTH else -1)
            if 0 <= y + distance < limit.h:
                return MowerPosition(x, y + distance, o)
            elif y + distance <= 0:
                return x, 0, o
            elif y + distance > limit.h:
                return MowerPosition(x, limit.h - 1, o)
        if o == OrdinalDirection.EAST or o == OrdinalDirection.WEST:
            distance *= (1 if o == OrdinalDirection.EAST else -1)
            if 0 <= y + distance < limit.w:
                return MowerPosition(x + distance, y, o)
            elif y + distance <= 0:
                return 0, y, o
            elif y + distance > limit.w:
                return MowerPosition(limit.w - 1, y, o)

    @staticmethod
    def rotate_mower_position(mower_position: MowerPosition, direction: RelativeDirection) -> MowerPosition:
        """Rotate mower position."""
        if direction not in (RelativeDirection.LEFT, RelativeDirection.RIGHT):
            raise MowerModelError(value=direction, message=f'Mower cannot be rotate with a {direction} direction.')
        x, y, o = mower_position
        orientations = [OrdinalDirection.NORTH, OrdinalDirection.EAST, OrdinalDirection.SOUTH, OrdinalDirection.WEST]
        if direction == RelativeDirection.LEFT:
            orientations = cycle(reversed(orientations))
        elif direction == RelativeDirection.RIGHT:
            orientations = cycle(orientations)
        for actual_orientation in orientations:
            if o == actual_orientation:
                return x, y, next(orientations)
