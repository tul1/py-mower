import pytest

from unittest import TestCase

from mower.resources.models.lawn_model import LawnModel
from mower.utils.exceptions import LawnModelLoadError

class TestLawnModel(TestCase):
    """LawnModel Test"""
    def test_from_str(self):
        # Given
        raw_lawn = '3 3'
        raw_lawn_with_spaces_at_begining = '  3 3'
        raw_lawn_with_spaces_at_end = '3 3  '
        raw_lawn_with_extra_spaces = ' 3   3  '


        # When
        lawn_1 = LawnModel.from_str(raw_lawn)
        lawn_2 = LawnModel.from_str(raw_lawn_with_spaces_at_begining)
        lawn_3 = LawnModel.from_str(raw_lawn_with_spaces_at_end)
        lawn_4 = LawnModel.from_str(raw_lawn_with_extra_spaces)

        # Then
        expected_lawn = LawnModel(height=3, width=3)

        self.assertEquals(expected_lawn, lawn_1)
        self.assertEquals(expected_lawn, lawn_2)
        self.assertEquals(expected_lawn, lawn_3)
        self.assertEquals(expected_lawn, lawn_4)

    def test_from_str_raises_on_wrong_input(self):
        # Given
        raw_lawn_with_one_param = '3'
        raw_lawn_with_one_param_and_spaces = ' 3 '
        raw_lawn_with_char = '3 e'
        raw_lawn_with_three_params = ' 3 2 2'
        raw_lawn_with_different_separator = '3|2'
        

        # When / Then
        self.assertRaises(LawnModelLoadError,
                          LawnModel.from_str,
                          raw_lawn_with_one_param)
        self.assertRaises(LawnModelLoadError,
                          LawnModel.from_str,
                          raw_lawn_with_one_param_and_spaces)
        self.assertRaises(LawnModelLoadError,
                          LawnModel.from_str,
                          raw_lawn_with_char)
        self.assertRaises(LawnModelLoadError,
                          LawnModel.from_str,
                          raw_lawn_with_three_params)
        self.assertRaises(LawnModelLoadError,
                          LawnModel.from_str,
                          raw_lawn_with_different_separator)
        