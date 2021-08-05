import re

from abc import ABC, abstractmethod
from typing import Tuple, Dict

from mower.resources.models.lawn_model import LawnModel
from mower.resources.models.mower_model import MowerModel, MowerPosition
from mower.resources.models.directions import OrdinalDirection
from mower.resources.models.position_model import Position
from mower.utils.exceptions import LoadFileParserError


class MowerParserService(ABC):
    """Parser Base Class."""
    @abstractmethod
    def parse(self) -> Tuple[Dict[Position, MowerModel], LawnModel]:
        pass


class FileMowerParserService(MowerParserService):
    """Implementation of file MowerParserService."""
    EMPTY_LINE_PATTERN = re.compile(r'^\s*$')
    LAWN_LINE_PATTERN = re.compile(r'^([\s]*)([0-9]+?)([\s]+)([0-9]+?)([\s]*)$')
    MOWER_INITIAL_POSITION_LINE_PATTERN = re.compile(r'^([\s]*)([0-9]+?)([\s]+)([0-9]+?)([\s]+)([NSWE])([\s]*)$')
    MOWER_DIRECTIONS_LINE_PATTERN = re.compile(r'^([LFBR\s]*)$')

    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    @staticmethod
    def parse_lawn(line: str) -> LawnModel:
        """Parse lawn string."""
        return LawnModel.from_str(line)

    @staticmethod
    def parse_mower_position(mowers: Dict[Position, MowerModel], lawn: LawnModel, line: str) -> Tuple[Position, Dict[Position, MowerModel]]:
        """Parse mower position string."""
        x, y, o = MowerModel.position_from_str(line)
        if x > lawn.width or y > lawn.height or y <= 0 or x <= 0:
            raise LoadFileParserError(value=line,
                                      message=f'Error while parsing input Mower file. Mower is outside the Lawn.')
        if (pos_xy := Position(x, y)) not in mowers:
            mowers[pos_xy] = MowerModel(position=(x, y, o))
            return pos_xy, mowers
        else:
            raise LoadFileParserError(value=line,
                                      message=f'Error while parsing input Mower file. Two mowers with the same position: {pos_xy}.')

    @staticmethod
    def parse_mower_directions(mowers: Dict[Position, MowerModel], pos_xy: Position, line: str) -> Dict[Position, MowerModel]:
        """Parse mower directions string."""
        try:
            mowers[pos_xy] = MowerModel.extend_directions_from_str(mowers[pos_xy], line)
            return mowers
        except KeyError:
            raise LoadFileParserError(value=line,
                                      message='Error while parsing input Mower file. No mower initial position has been declared.')

    def parse(self) -> Tuple[Dict[Position, MowerModel], LawnModel]:
        """Load mowers and lanw from file."""
        mowers: Dict[Position, MowerModel] = dict()
        lawn: LawnModel = None
        lawn_params_is_set: bool = False
        mower_position_xy: Position = None
        with open(self.filename, 'rt') as mower_file:
            for line in mower_file:
                if self.EMPTY_LINE_PATTERN.match(line):
                    # Skip empty line
                    continue
                if self.LAWN_LINE_PATTERN.match(line) and not lawn_params_is_set:
                    lawn = FileMowerParserService.parse_lawn(line)
                    lawn_params_is_set = True
                elif self.MOWER_INITIAL_POSITION_LINE_PATTERN.match(line) and lawn_params_is_set:
                    mower_position_xy, mowers = FileMowerParserService.parse_mower_position(mowers, lawn, line)
                elif self.MOWER_DIRECTIONS_LINE_PATTERN.match(line) and lawn_params_is_set:
                    mowers = FileMowerParserService.parse_mower_directions(mowers, mower_position_xy, line)
                else:
                    raise LoadFileParserError(value=line, message='Error while parsing input Mower file.')
        if lawn is None:
            raise LoadFileParserError(value=lawn, message='Error while parsing input Mower file. Empty input file.')
        return mowers, lawn


class StdinMowerParserService(MowerParserService):
    """Class Stdin Mower Parser Service."""
    def parse(self) -> Tuple[Dict[Position, MowerModel], LawnModel]:
        """Load mowers and lanw from stdin."""
        mowers: Dict[Position, MowerModel] = dict()
        lawn: LawnModel = None
        return mowers, lawn
