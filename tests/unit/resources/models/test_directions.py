import pytest

from unittest import TestCase

from mower.resources.models.directions import RelativeDirection, OrdinalDirection
from mower.utils.exceptions import RelativeDirectionError, OrdinalDirectionError


class TestDirections(TestCase):
    """Directions Test"""

    def test_ordinal_direction_from_str(self):
        """Test ordinal direction from string builder."""
        self.assertIs(OrdinalDirection.NORTH, OrdinalDirection.from_str('N'))
        self.assertIs(OrdinalDirection.SOUTH, OrdinalDirection.from_str('S'))
        self.assertIs(OrdinalDirection.EAST, OrdinalDirection.from_str('E'))
        self.assertIs(OrdinalDirection.WEST, OrdinalDirection.from_str('W'))

    def test_ordinal_direction_str(self):
        """Test ordinal direction str representational method."""
        self.assertEquals('N', str(OrdinalDirection.NORTH))
        self.assertEquals('S', str(OrdinalDirection.SOUTH))
        self.assertEquals('E', str(OrdinalDirection.EAST))
        self.assertEquals('W', str(OrdinalDirection.WEST))

    def test_ordinal_direction_raises_on_wrong_input(self):
        """Test ordinal direction when a wrong input is passed."""
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, '')
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, ' ')
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, 'd')
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, 'ffff')
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, 's')
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, 'n')
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, 'w')
        self.assertRaises(OrdinalDirectionError, OrdinalDirection.from_str, 'e')

    def test_relative_direction_from_str(self):
        """Test relative direction from string builder."""
        self.assertIs(RelativeDirection.FRONT, RelativeDirection.from_str('F'))
        self.assertIs(RelativeDirection.BACK, RelativeDirection.from_str('B'))
        self.assertIs(RelativeDirection.LEFT, RelativeDirection.from_str('L'))
        self.assertIs(RelativeDirection.RIGHT, RelativeDirection.from_str('R'))
    
    def test_ordinal_direction_str(self):
        """Test relative direction str representational method."""
        self.assertEquals('F', str(RelativeDirection.FRONT))
        self.assertEquals('B', str(RelativeDirection.BACK))
        self.assertEquals('L', str(RelativeDirection.LEFT))
        self.assertEquals('R', str(RelativeDirection.RIGHT))

    def test_relative_direction_raises_on_wrong_input(self):
        """Test ordinal direction"""
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, '')
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, ' ')
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, 'd')
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, 'ffff')
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, 's')
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, 'n')
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, 'w')
        self.assertRaises(RelativeDirectionError, RelativeDirection.from_str, 'e')

