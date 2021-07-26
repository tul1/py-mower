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
    def parse(self) -> Tuple[Dict[int, MowerModel], LawnModel]:
        pass


class FileMowerParserService(MowerParserService):
    """Implementation of file MowerParserService."""
    EMPTY_LINE_PATTERN = re.compile(r'^\s*$')
    LAWN_LINE_PATTERN = re.compile(r'^([\s]*)([0-9]+?)([\s]+)([0-9]+?)([\s]*)$')
    MOWER_INITIAL_POSITION_LINE_PATTERN = re.compile(r'^([\s]*)([0-9]+?)([\s]+)([0-9]+?)([\s]+)([NSWE]?)([\s]*)$')
    MOWER_DIRECTIONS_LINE_PATTERN = re.compile(r'^([LFBR\s]*)$')

    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def parse(self) -> Tuple[Dict[int, MowerModel], LawnModel]:
        """Load mowers and lanw from file."""
        mowers: Dict[int, MowerModel] = dict()
        lawn: LawnModel = None
        lawn_params_is_set: bool = False
        initial_position: Tuple[int, int, OrdinalDirection] = None
        with open(self.filename, 'rt') as mower_file:
            for line in mower_file:
                if self.EMPTY_LINE_PATTERN.match(line):
                    # Skip empty line
                    continue
                if self.LAWN_LINE_PATTERN.match(line) and lawn_params_is_set == False:
                    lawn = LawnModel.from_str(line)
                    lawn_params_is_set = True
                elif self.MOWER_INITIAL_POSITION_LINE_PATTERN.match(line):
                    if (initial_position := MowerModel.mower_position_from_str(line)) not in mowers:
                        mowers[initial_position] = MowerModel.from_initial_position(initial_position)
                    else:
                        raise LoadFileParserError(value=line,
                                                  message=f'Error while parsing input Mower file. Two mowers with the same position: {initial_position}.')
                elif self.MOWER_DIRECTIONS_LINE_PATTERN.match(line):
                    try:
                        mowers[initial_position] = MowerModel.extend_directions_from_str(mowers[initial_position], line)
                    except KeyError:
                        LoadFileParserError(value=line, message='Error while parsing input Mower file. No mower initial position has been declared.')
                else:
                    raise LoadFileParserError(value=line, message='Error while parsing input Mower file.')
        return mowers, lawn


