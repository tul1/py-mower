import pytest

from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open

from mower.resources.services.mower_parsers_service import FileMowerParserService
from mower.utils.exceptions import LoadFileParserError


def lawn_from_str(h_w):
    """Function to mock to build lawn from string."""
    return MagicMock(height_width=h_w)

def mower_pos_mock(position):
    """Function to mock mower position from string."""
    return position

def mower_from_init_pos_mock(position):
    """Function to mock to build mower from string with position."""
    return MagicMock(position=position)

def mower_extend_dir_mock(mock, directions):
    """Function to mock to build mower from string with mower base and directions."""
    if len(mock.directions) == 0:
        mock.directions = directions
    else:
        mock.directions += directions
    return mock

def assert_parse_method_raises_custom_exception(method_input, expected_exception, assert_method):
    """Helper function to assert specific exception for parser method."""
    parser = FileMowerParserService('filename')
    text_file_data = '\n'.join(method_input)
    with patch('mower.resources.services.mower_parsers_service.open',
                mock_open(read_data=text_file_data), create=True) as file_mock:
        file_mock.return_value.__iter__.return_value = text_file_data.splitlines()
        assert_method(expected_exception, parser.parse)

def patch_and_run_parse_method(method_input, mower_mock, lawn_mock):
    """Helper function patch parser method."""
    lawn_mock.from_str = lawn_from_str
    mower_mock.extend_directions_from_str = mower_extend_dir_mock
    mower_mock.mower_position_from_str = mower_pos_mock
    mower_mock.from_initial_position = mower_from_init_pos_mock
    parser = FileMowerParserService('filename')
    with patch('mower.resources.services.mower_parsers_service.open',
            mock_open(read_data=method_input), create=True) as file_mock:
        file_mock.return_value.__iter__.return_value = method_input.splitlines()
        return parser.parse()


@patch('mower.resources.services.mower_parsers_service.LawnModel')
@patch('mower.resources.services.mower_parsers_service.MowerModel')
class TestFileMowerParserService(TestCase):
    """Mower test"""
    def test_parse_empty_file(self, mower_mock, lawn_mock):
        """Test parse a mower file."""
        # Given / When
        mowers, lawn = patch_and_run_parse_method('\n'.join([' ']), mower_mock, lawn_mock)

        # Then
        self.assertEquals(dict(), mowers)
        self.assertIsNone(lawn)

    def test_parse_file_with_no_mower(self, mower_mock, lawn_mock):
        """Test parse a mower file."""
        # Given / When
        mowers, lawn = patch_and_run_parse_method('\n'.join(['4 4']), mower_mock, lawn_mock)

        # Then
        expected_lawn = MagicMock(height_width='4 4')

        self.assertEquals(dict(), mowers)
        self.assertEquals(expected_lawn.height_width, lawn.height_width)

    def test_parse_file_with_single_mower(self, mower_mock, lawn_mock):
        """Test parse a mower file."""
        # Given / When
        mowers, lawn = patch_and_run_parse_method('\n'.join(['4 4', '2 2 N', 'LBFR']),
                                                  mower_mock, lawn_mock)

        # Then
        expected_mowers = {0: MagicMock(position='2 2 N\n', directions='LBFR')}
        expected_lawn = MagicMock(height_width='4 4\n')

        self.assertEquals(expected_mowers[0].position, mowers['2 2 N\n'].position)
        self.assertEquals(expected_mowers[0].directions, mowers['2 2 N\n'].directions)
        self.assertEquals(expected_lawn.height_width, lawn.height_width)

    def test_parse_file_with_multiplemowers_mower_with_no_directions(self, mower_mock, lawn_mock):
        """Test parse a mower file."""
        # Given / When
        mowers, lawn = patch_and_run_parse_method('\n'.join(['4 4', '1 2 E', '2 3 S', '4 4 N', '1 1 W']),
                                                  mower_mock, lawn_mock)

        # Then
        expected_mowers = {'1 2 E\n': MagicMock(position='1 2 E\n'), '2 3 S\n': MagicMock(position='2 3 S\n'),
                           '4 4 N\n': MagicMock(position='4 4 N\n'), '1 1 W': MagicMock(position='1 1 W')}
        expected_lawn = MagicMock(height_width='4 4\n')

        self.assertEquals(expected_lawn.height_width, lawn.height_width)
        for key, mower in expected_mowers.items():
            self.assertEquals(mower.position, mowers[key].position)
            self.assertEqual(0, len(mowers[key].directions))

    def test_parse_file_with_single_mower_with_multiline_directions(self, mower_mock, lawn_mock):
        """Test parse a mower file with multiple line directions."""
        # Given / When
        mowers, lawn = patch_and_run_parse_method('\n'.join(['4 4', '2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB']),
                                                  mower_mock, lawn_mock)

        # Then
        expected_mowers = {0: MagicMock(position='2 2 N\n', directions='LBFR\nL\nF\nRRRLLBB')}
        expected_lawn = MagicMock(height_width='4 4\n')

        self.assertEquals(expected_mowers[0].position, mowers['2 2 N\n'].position)
        self.assertEquals(expected_mowers[0].directions, mowers['2 2 N\n'].directions)
        self.assertEquals(expected_lawn.height_width, lawn.height_width)

    def test_parse_file_with_multiple_mowers_with_multiline_directions(self, mower_mock, lawn_mock):
        """Test parse a mower file with multiple line directions."""
        # Given / When
        mowers, lawn = patch_and_run_parse_method('\n'.join(['4 4', '2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB', '3 3 E', 'RRR', '5 5 S']),
                                                  mower_mock, lawn_mock)

        # Then
        expected_mowers = {'2 2 N\n': MagicMock(position='2 2 N\n', directions='LBFR\nL\nF\nRRRLLBB\n'),
                           '3 3 E\n': MagicMock(position='3 3 E\n', directions='RRR\n'),
                           '5 5 S': MagicMock(position='5 5 S')}
        expected_lawn = MagicMock(height_width='4 4\n')

        self.assertEquals(expected_lawn.height_width, lawn.height_width)

        for key, mower in expected_mowers.items():
            self.assertEquals(mower.position, mowers[key].position)
            if len(mowers[key].directions) != 0:
                self.assertEquals(mower.directions, mowers[key].directions)
            else:
                self.assertEqual(0, len(mowers[key].directions))

    def test_parse_raises_on_single_mower_with_no_init_pos(self, _, __):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['4 4', 'LBFR', 'L', 'F', 'RRRLLBB'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_on_single_mower_with_two_lawn_params(self, _, __):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['4 4', '4 4', 'LBFR', 'L', 'F', 'RRRLLBB'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_with_no_lawn_params_nor_init_mower_pos(self, _, __):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['LBFR', 'L', 'F', 'RRRLLBB'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_on_with_no_lawn_params(self, _, __):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_on_two_mower_with_same_init_position(self, _, __):
        """Test parse mower raises error on wrong mower file data."""
        with self.assertRaises(LoadFileParserError):
            patch_and_run_parse_method('\n'.join(['4 4', '2 2 N', '2 2 S', 'LB']),
                                       mower_mock, lawn_mock)

    def test_parse_raises_on_mower_outside_lawn(self, _, __):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['2 2', '4 4 S'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)
