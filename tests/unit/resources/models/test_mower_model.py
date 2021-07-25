import pytest

from unittest import TestCase

from mower.resources.models.directions import RelativeDirection
from mower.resources.models.mower_model import MowerModel
from mower.utils.exceptions import MowerModelLoadError


class TestMowerModel(TestCase):
    """MowerModel Test."""
    def test_build_mower_relative_directions(self):
        # Given
        raw_directions = 'L FRB BRF LL FFR R'

        # When
        mower_model = MowerModel.add_directions_from_str(raw_directions)
        
        # Then
        expected_directions = [RelativeDirection.LEFT, RelativeDirection.FRONT, RelativeDirection.RIGHT, RelativeDirection.BACK,
                               RelativeDirection.BACK, RelativeDirection.RIGHT, RelativeDirection.FRONT, RelativeDirection.LEFT,
                               RelativeDirection.LEFT, RelativeDirection.FRONT, RelativeDirection.FRONT, RelativeDirection.RIGHT,
                               RelativeDirection.RIGHT]

        self.assertEquals(expected_directions, mower_model.direct)

    def test_build_mower_relative_directions_returns_empty_list_on_none_directions_input(self):
        # Given
        raw_directions = ' '

        # When
        directions = Mower.build_mower_relative_directions_from_str(raw_directions)
        
        # Then
        expected_directions = []

        self.assertEquals(expected_directions, directions)