from __future__ import annotations
from pydantic import BaseModel
from typing import Tuple, List, Optional

from mower.resources.models.directions import OrdinalDirection, RelativeDirection


class MowerModel(BaseModel):
    """Mower model."""

    position: Tuple[int, int, OrdinalDirection]
    directions: Optional[List[RelativeDirection]]

    @classmethod
    def from_initial_position_str(cls: MowerModel, mower_init_pos_input: str) -> MowerModel:
        """Build mower from initial position formatted string."""
        try:
            h, w, d = mower_init_pos_input.split()
            return MowerModel(position=(int(h), int(w), CardinalDirection.from_str(d)),
                              directions=list())
        except ValueError:
            raise MowerModelLoadError(value=mower_init_pos_input, message='Wrong Mower initial position params in the input file.')

    def add_directions_from_str(self, relative_directions: str) -> List[RelativeDirection]:
        """Builds mower realative directions list from string."""
        new_directions = [RelativeDirection.from_str(direction) for direction in relative_directions if direction != ' ']
        if self.directions:
            self.directions.extend(new_directions)
        else:
            self.directions = new_directions