import re

from abc import ABC, abstractmethod
from typing import Tuple, Dict

from mower.resources.models.lawn_model import LawnModel
from mower.resources.models.mower_model import MowerModel
from mower.resources.models.directions import OrdinalDirection
from mower.utils.exceptions import LoadFileParserError


class MowerParserService(ABC):
    """Parser Interface."""
    @abstractmethod
    def parse(self) -> Tuple[Dict[Tuple[int, int], MowerModel], LawnModel]:
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
    def parse_mower_position(mowers: Dict[Tuple[int, int], MowerModel], lawn: LawnModel, line: str) -> Tuple[Tuple[int, int], Dict[Tuple[int, int], MowerModel]]:
        """Parse mower position string."""
        x, y, _ = MowerModel.mower_position_from_str(line)
        if x > lawn.width or y > lawn.height or y <= 0 or x <= 0:
            raise LoadFileParserError(value=line,
                                      message=f'Error while parsing input Mower file. Mower is outside the Lawn.')
        if (pos_xy := (x, y)) not in mowers:    
            mowers[pos_xy] = MowerModel.from_initial_position(pos_xy)
            return pos_xy, mowers
        else:
            raise LoadFileParserError(value=line,
                                      message=f'Error while parsing input Mower file. Two mowers with the same position: {pos_xy}.')

    @staticmethod
    def parse_mower_directions(mowers: Dict[Tuple[int, int], MowerModel], pos_xy: Tuple[int, int], line: str) -> Dict[Tuple[int, int], MowerModel]:
        """Parse mower directions string."""
        try:
            mowers[pos_xy] = MowerModel.extend_directions_from_str(mowers[pos_xy], line)
            return mowers
        except KeyError:
            raise LoadFileParserError(value=line,
                                      message='Error while parsing input Mower file. No mower initial position has been declared.')

    def parse(self) -> Tuple[Dict[Tuple[int, int], MowerModel], LawnModel]:
        """Load mowers and lanw from file."""
        mowers: Dict[Tuple[int, int], MowerModel] = dict()
        lawn: LawnModel = None
        lawn_params_is_set: bool = False
        mower_position_xy: Tuple[int, int] = None
        with open(self.filename, 'rt') as mower_file:
            for line in mower_file:
                if self.EMPTY_LINE_PATTERN.match(line):
                    # Skip empty line
                    continue
                if self.LAWN_LINE_PATTERN.match(line) and lawn_params_is_set == False:
                    lawn = FileMowerParserService.parse_lawn(line)
                    lawn_params_is_set = True
                elif self.MOWER_INITIAL_POSITION_LINE_PATTERN.match(line) and lawn_params_is_set == True:
                    mower_position_xy, mowers = FileMowerParserService.parse_mower_position(mowers, lawn, line)
                elif self.MOWER_DIRECTIONS_LINE_PATTERN.match(line) and lawn_params_is_set == True:
                    mowers = FileMowerParserService.parse_mower_directions(mowers, mower_position_xy, line)
                else:
                    raise LoadFileParserError(value=line, message='Error while parsing input Mower file.')
        if lawn is None:
             raise LoadFileParserError(value=lawn, message='Error while parsing input Mower file. Empty input file.')
        return mowers, lawn


