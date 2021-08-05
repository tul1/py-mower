import pytest

from unittest import TestCase

from mower.resources.models.directions import RelativeDirection, OrdinalDirection
from mower.resources.models.mower_model import MowerModel, MowerPosition
from mower.resources.models.lawn_model import LawnDimensions
from mower.utils.exceptions import MowerModelLoadError, MowerModelError


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

    def test_translate_mower_position_moving_foreward(self):
        """Test when translate mower foreward."""
        # Mower moves 1 position
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.NORTH),
                                                       1,
                                                       RelativeDirection.FRONT,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 2, OrdinalDirection.NORTH), position)

        # Mower moves 1 position
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.NORTH),
                                                       -1,
                                                       RelativeDirection.FRONT,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 2, OrdinalDirection.NORTH), position)

        # Mower reaches upper limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.NORTH),
                                                       10,
                                                       RelativeDirection.FRONT,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 4, OrdinalDirection.NORTH), position)

        # Mower reaches lower limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.SOUTH),
                                                       10,
                                                       RelativeDirection.FRONT,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 0, OrdinalDirection.SOUTH), position)

        # Mower reaches further right limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.EAST),
                                                       10,
                                                       RelativeDirection.FRONT,
                                                       LawnDimensions(3, 5))
        self.assertEquals((2, 1, OrdinalDirection.EAST), position)

        # Mower reaches further left limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.WEST),
                                                       10,
                                                       RelativeDirection.FRONT,
                                                       LawnDimensions(3, 5))
        self.assertEquals((0, 1, OrdinalDirection.WEST), position)

    def test_translate_mower_position_moving_backward(self):
        """Test when translate mower backward."""
        # Mower moves 1 position
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.NORTH),
                                                       1,
                                                       RelativeDirection.BACK,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 0, OrdinalDirection.NORTH), position)

        # Mower moves 1 position
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.NORTH),
                                                       -1,
                                                       RelativeDirection.BACK,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 0, OrdinalDirection.NORTH), position)

        # Mower reaches upper limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.NORTH),
                                                       10,
                                                       RelativeDirection.BACK,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 0, OrdinalDirection.NORTH), position)

        # Mower reaches lower limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.SOUTH),
                                                       10,
                                                       RelativeDirection.BACK,
                                                       LawnDimensions(3, 5))
        self.assertEquals((1, 4, OrdinalDirection.SOUTH), position)

        # Mower reaches further right limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.EAST),
                                                       10,
                                                       RelativeDirection.BACK,
                                                       LawnDimensions(3, 5))
        self.assertEquals((0, 1, OrdinalDirection.EAST), position)

        # Mower reaches further left limit
        position = MowerModel.translate_mower_position(MowerPosition(1, 1, OrdinalDirection.WEST),
                                                       10,
                                                       RelativeDirection.BACK,
                                                       LawnDimensions(3, 5))
        self.assertEquals((2, 1, OrdinalDirection.WEST), position)

    def test_translate_mower_position_raises_MowerModelError(self):
        """Test when translate raises exception because of wrong direction."""
        self.assertRaises(MowerModelError,
                          MowerModel.translate_mower_position,
                          (1, 1, OrdinalDirection.NORTH),
                          10,
                          RelativeDirection.LEFT,
                          (2, 2))
        self.assertRaises(MowerModelError,
                          MowerModel.translate_mower_position,
                          (1, 1, OrdinalDirection.NORTH),
                          10,
                          RelativeDirection.RIGHT,
                          (2, 2))

    def test_rotate_mower_position_clockwise(self):
        """Test when rotate raises exception because of wrong direction."""
        # Rotate North to East
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.NORTH),
                                                    RelativeDirection.RIGHT)
        self.assertEquals((1, 1, OrdinalDirection.EAST), position)

        # Rotate East to South
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.EAST),
                                                    RelativeDirection.RIGHT)
        self.assertEquals((1, 1, OrdinalDirection.SOUTH), position)

        # Rotate South to West
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.SOUTH),
                                                    RelativeDirection.RIGHT)
        self.assertEquals((1, 1, OrdinalDirection.WEST), position)

        # Rotate West to North
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.WEST),
                                                    RelativeDirection.RIGHT)
        self.assertEquals((1, 1, OrdinalDirection.NORTH), position)

    def test_rotate_mower_position_anticlockwise(self):
        """Test when rotate raises exception because of wrong direction."""
        # Rotate North to West
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.NORTH),
                                                    RelativeDirection.LEFT)
        self.assertEquals((1, 1, OrdinalDirection.WEST), position)

        # Rotate West to South
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.WEST),
                                                    RelativeDirection.LEFT)
        self.assertEquals((1, 1, OrdinalDirection.SOUTH), position)

        # Rotate South to East
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.SOUTH),
                                                    RelativeDirection.LEFT)
        self.assertEquals((1, 1, OrdinalDirection.EAST), position)

        # Rotate East to North
        position = MowerModel.rotate_mower_position((1, 1, OrdinalDirection.EAST),
                                                    RelativeDirection.LEFT)
        self.assertEquals((1, 1, OrdinalDirection.NORTH), position)

    def test_rotate_mower_position_raises_MowerModelError(self):
        """Test when rotate raises exception because of wrong direction."""
        self.assertRaises(MowerModelError,
                          MowerModel.rotate_mower_position,
                          (1, 1, OrdinalDirection.NORTH),
                          RelativeDirection.BACK)
        self.assertRaises(MowerModelError,
                          MowerModel.rotate_mower_position,
                          (1, 1, OrdinalDirection.NORTH),
                          RelativeDirection.FRONT)
