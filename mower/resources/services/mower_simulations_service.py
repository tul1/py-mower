from abc import ABC, abstractmethod
from typing import Set, Tuple, Dict

from mower.resources.models.directions import RelativeDirection, OrdinalDirection
from mower.resources.models.lawn_model import LawnModel
from mower.resources.models.mower_model import MowerModel


class MowerSimulationService(ABC):
    """Simulation Base Class."""
    @abstractmethod
    def run(self, mowers: Dict[Tuple[int, int], MowerModel], lawn: LawnModel) -> Set[MowerModel]:
        pass


class SyncMowerSimulationService(MowerSimulationService):
    """Synchronous simulation class."""
    @staticmethod
    def move_mower(mowers: Dict[Tuple[int, int], MowerModel], mower: MowerModel, lawn: LawnModel) -> Dict[Tuple[int, int], MowerModel]:
        """Mover mower in lawn."""
        direction = mower.directions.pop(0)
        lawn_limits = lawn.width, lawn.height
        position = mower.position
        if direction in (RelativeDirection.FRONT, RelativeDirection.BACK):
            position = MowerModel.translate_mower_position(position, 1, direction, lawn_limits)
        elif direction in (RelativeDirection.LEFT, RelativeDirection.RIGHT):
            position = MowerModel.rotate_mower_position(position, direction)
        if (pos := position.x, position.y) in mowers:
            mower.position = position
            mowers[pos] = mower
        return mowers

    def run(self, mowers: Dict[Tuple[int, int], MowerModel], lawn: LawnModel) -> Set[MowerModel]:
        """Run simulation with in a lawn with several mowers."""
        output_mowers: Set[MowerModel] = set()
        while len(mowers) > len(output_mowers):
            for mower in mowers:
                if not mower.directions:
                    output_mowers.add(mower)
                else:
                    mowers = SyncMowerSimulationService.move_mower(mowers, mower, lawn)
        return output_mowers


class AsyncMowerSimulationService(MowerSimulationService):
    """Asynchronous simulation class."""
    def run(self, mowers: Dict[Tuple[int, int], MowerModel], lawn: LawnModel) -> Set[MowerModel]:
        pass
