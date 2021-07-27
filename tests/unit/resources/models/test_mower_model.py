import pytest

from unittest import TestCase

from mower.resources.models.directions import RelativeDirection, OrdinalDirection
from mower.resources.models.mower_model import MowerModel
from mower.utils.exceptions import MowerModelLoadError


class TestMowerModel(TestCase):
    """MowerModel Test."""
    def test_from_initial_position_str(self):
        """Test building a mower model from initial position string."""
        # Given
        raw_init_pos = '  2   2 N  '

        # When
        mower_model = MowerModel.from_initial_position_str(raw_init_pos)

        # Then
        expected_position = (2, 2, OrdinalDirection.NORTH)

        self.assertEqual(expected_position, mower_model.position)
        self.assertEqual([], mower_model.directions)

    def test_from_initial_position_str_raises_on_wrong_direction(self):
        """Test building a mower model from initial position string."""
        self.assertRaises(MowerModelLoadError,
                          MowerModel.from_initial_position_str,
                          '   ')
        self.assertRaises(MowerModelLoadError,
                          MowerModel.from_initial_position_str,
                          '2 d N')
        self.assertRaises(MowerModelLoadError,
                          MowerModel.from_initial_position_str,
                          'e 3 N')
        self.assertRaises(MowerModelLoadError,
                          MowerModel.from_initial_position_str,
                          '2 3 2')
        self.assertRaises(MowerModelLoadError,
                          MowerModel.from_initial_position_str,
                          'adsasdasdasd')
        self.assertRaises(MowerModelLoadError,
                          MowerModel.from_initial_position_str,
                          '2223123123')
        self.assertRaises(MowerModelLoadError,
                          MowerModel.from_initial_position_str,
                          '22222222222 2222222332 NSADS')

    def test_extend_directions_from_str(self):
        """Test extend direction to mower model from string."""
        # Given
        raw_directions = '  L FR  B BRF LL FFR R  '
        mower_model = MowerModel(position=(1, 1, OrdinalDirection.NORTH))

        # When
        mower_model = MowerModel.extend_directions_from_str(mower_model, raw_directions)
        
        # Then
        expected_directions = [RelativeDirection.LEFT, RelativeDirection.FRONT, RelativeDirection.RIGHT, RelativeDirection.BACK,
                               RelativeDirection.BACK, RelativeDirection.RIGHT, RelativeDirection.FRONT, RelativeDirection.LEFT,
                               RelativeDirection.LEFT, RelativeDirection.FRONT, RelativeDirection.FRONT, RelativeDirection.RIGHT,
                               RelativeDirection.RIGHT]

        self.assertEquals(expected_directions, mower_model.directions)

    def test_extend_directions_from_str_returns_base_direction_list_on_none_directions_input(self):
        """Test extend directions from string when empty direction but base mower has directions."""
        # Given
        raw_directions = ' '
        mower_model = MowerModel(position=(1, 1, OrdinalDirection.NORTH),
                                 directions=[RelativeDirection.BACK, RelativeDirection.FRONT])

        # When
        mower_model = MowerModel.extend_directions_from_str(mower_model, raw_directions)
        
        # Then
        expected_directions = [RelativeDirection.BACK, RelativeDirection.FRONT]

        self.assertEquals(expected_directions, mower_model.directions)

    def test_extend_directions_from_str_returns_empty_list_on_none_directions_input(self):
        """Test extend directions from string when empty direction."""
        # Given
        raw_directions = ' '
        mower_model = MowerModel(position=(1, 1, OrdinalDirection.NORTH))

        # When
        mower_model = MowerModel.extend_directions_from_str(mower_model, raw_directions)
        
        # Then
        expected_directions = []

        self.assertEquals(expected_directions, mower_model.directions)
