from abc import ABC, abstractmethod
from typing import Set, Tuple, Dict

from mower.resources.models.directions import RelativeDirection, OrdinalDirection
from mower.resources.models.lawn_model import LawnModel, LawnDimensions
from mower.resources.models.mower_model import MowerModel
from mower.resources.models.position_model import Position

class MowerSimulationService(ABC):
    """Simulation Base Class."""
    @abstractmethod
    def run(self, mowers: Dict[Position, MowerModel], lawn: LawnModel) -> Set[MowerModel]:
        pass


class SyncMowerSimulationService(MowerSimulationService):
    """Synchronous simulation class."""
    @staticmethod
    def move_mower(mowers: Dict[Position, MowerModel], mower: MowerModel, lawn_dims: LawnDimensions) -> Dict[Position, MowerModel]:
        """Mover mower in lawn."""
        direction = mower.directions.pop(0)
        position = mower.position
        if direction in (RelativeDirection.FRONT, RelativeDirection.BACK):
            position = MowerModel.translate_mower_position(position, 1, direction, lawn_dims)
        elif direction in (RelativeDirection.LEFT, RelativeDirection.RIGHT):
            position = MowerModel.rotate_mower_position(position, direction)
        if (pos := position.x, position.y) in mowers:
            mower.position = position
            mowers[pos] = mower
        return mowers

    def run(self, mowers: Dict[Position, MowerModel], lawn: LawnModel) -> Set[MowerModel]:
        """Run simulation with in a lawn with several mowers."""
        output_mowers: Set[MowerModel] = set()
        while len(mowers) > len(output_mowers):
            for mower in mowers:
                if not mower.directions:
                    output_mowers.add(mower)
                else:
                    mowers = SyncMowerSimulationService.move_mower(mowers, mower, lawn.as_tuple())
        return output_mowers


class AsyncMowerSimulationService(MowerSimulationService):
    """Asynchronous simulation class."""
    def run(self, mowers: Dict[Position, MowerModel], lawn: LawnModel) -> Set[MowerModel]:
        pass
