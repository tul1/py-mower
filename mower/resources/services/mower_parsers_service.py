import re

from abc import ABCMeta, abstractmethod
from typing import Tuple, Dict

from mower.resources.models.lawn_model import LawnModel
from mower.resources.models.mower_model import MowerModel
from mower.utils.exceptions import LoadFileParserError


class MowerParserService(ABCMeta):
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
        mower_counter: int = 0
        with open(self.filename, 'rt') as mower_file:
            for _, line in enumerate(mower_file):
                if self.EMPTY_LINE_PATTERN.match(line):
                    # Skip empty line
                    continue
                if self.LAWN_LINE_PATTERN.match(line):
                    # First line must be lawn params
                    lawn = LawnModel.from_str(line)
                elif self.MOWER_INITIAL_POSITION_LINE_PATTERN.match(line):
                    # Even lines must be mower initial position
                    mowers[mower_counter] = MowerModel.from_initial_position_str(line)
                    mower_counter += 1
                elif self.MOWER_DIRECTIONS_LINE_PATTERN.match(line):
                    # Odd lines must be mower
                    mowers[mower_counter].directions.add_from_str(line)
                else:
                    raise LoadFileParserError(value=line, message='')
        return mowers, lawn


