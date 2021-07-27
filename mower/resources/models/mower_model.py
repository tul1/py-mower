from __future__ import annotations
from pydantic import BaseModel
from typing import Tuple, List, Optional

from mower.resources.models.directions import OrdinalDirection, RelativeDirection
from mower.utils.exceptions import MowerModelLoadError, OrdinalDirectionError

class MowerModel(BaseModel):
    """Mower model."""

    position: Tuple[int, int, OrdinalDirection]
    directions: Optional[List[RelativeDirection]] = list()

    @staticmethod
    def mower_position_from_str(mower_pos_input: str) -> Tuple[int, int, OrdinalDirection]:
        """Build mower position."""
        try:
            h, w, d = mower_pos_input.split()
            return int(h), int(w), OrdinalDirection.from_str(d)
        except (ValueError, OrdinalDirectionError):
            raise MowerModelLoadError(value=mower_pos_input, message='Wrong Mower position params in the input file.')

    @classmethod
    def from_initial_position_str(cls: MowerModel, mower_init_pos_input: str) -> MowerModel:
        """Build mower from initial position formatted string."""
        return MowerModel(position=MowerModel.mower_position_from_str(mower_init_pos_input))

    @classmethod
    def from_initial_position(cls: MowerModel, mower_init_pos_input: Tuple[int, int, OrdinalDirection]) -> MowerModel:
        """Build mower from initial position formatted string."""
        return MowerModel(position=mower_init_pos_input)

    @classmethod
    def extend_directions_from_str(cls: MowerModel, base_model: MowerModel, relative_directions: str) -> List[RelativeDirection]:
        """Builds mower realative directions list from string."""
        base_directions = base_model.directions
        new_directions = [RelativeDirection.from_str(direction) for direction in relative_directions if direction != ' ']
        new_directions.extend(base_directions)
        return MowerModel(position=base_model.position, directions=new_directions)
