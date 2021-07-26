import pytest

from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open

from mower.resources.services.mower_parsers_service import FileMowerParserService
from mower.utils.exceptions import LoadFileParserError


def lawn_from_str(h_w):
    """Function to mock to build lawn from string."""
    return MagicMock(height_width=h_w)

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


@patch('mower.resources.services.mower_parsers_service.LawnModel')
@patch('mower.resources.services.mower_parsers_service.MowerModel')
class TestFileMowerParserService(TestCase):
    """Mower test"""
    def test_parse_file_with_single_mower(self, mower_mock, lawn_mock):
        """Test parse a mower file."""
        # Given
        parser = FileMowerParserService('filename')
        text_file_data = '\n'.join(['4 4', '2 2 N', 'LBFR'])
        lawn_mock.from_str = lawn_from_str
        mower_mock.extend_directions_from_str = mower_extend_dir_mock
        mower_mock.from_initial_position_str = mower_from_init_pos_mock

        # When
        with patch('mower.resources.services.mower_parsers_service.open',
                    mock_open(read_data=text_file_data), create=True) as file_mock:
            file_mock.return_value.__iter__.return_value = text_file_data.splitlines()
            mowers, lawn = parser.parse()

        # Then
        expected_mowers = {0: MagicMock(position='2 2 N\n', directions='LBFR')}
        expected_lawn = MagicMock(height_width='4 4\n')

        self.assertEquals(expected_mowers[0].position, mowers[0].position)
        self.assertEquals(expected_mowers[0].directions, mowers[0].directions)
        self.assertEquals(expected_lawn.height_width, lawn.height_width)

    def test_parse_file_with_single_mower_with_multiline_directions(self, mower_mock, lawn_mock):
        """Test parse a mower file with multiple line directions."""
        # Given
        parser = FileMowerParserService('filename')
        text_file_data = '\n'.join(['4 4', '2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB'])
        lawn_mock.from_str = lawn_from_str
        mower_mock.extend_directions_from_str = mower_extend_dir_mock
        mower_mock.from_initial_position_str = mower_from_init_pos_mock

        # When
        with patch('mower.resources.services.mower_parsers_service.open',
                    mock_open(read_data=text_file_data), create=True) as file_mock:
            file_mock.return_value.__iter__.return_value = text_file_data.splitlines()
            mowers, lawn = parser.parse()

        # Then
        expected_mowers = {0: MagicMock(position='2 2 N\n', directions='LBFR\nL\nF\nRRRLLBB')}
        expected_lawn = MagicMock(height_width='4 4\n')

        self.assertEquals(expected_mowers[0].position, mowers[0].position)
        self.assertEquals(expected_mowers[0].directions, mowers[0].directions)
        self.assertEquals(expected_lawn.height_width, lawn.height_width)

    def test_parse_file_with_multiple_mowers_with_multiline_directions(self, mower_mock, lawn_mock):
        """Test parse a mower file with multiple line directions."""
        # Given
        parser = FileMowerParserService('filename')
        text_file_data = '\n'.join(['4 4', '2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB', '3 3 E', 'RRR', '5 5 S'])
        lawn_mock.from_str = lawn_from_str
        mower_mock.extend_directions_from_str = mower_extend_dir_mock
        mower_mock.from_initial_position_str = mower_from_init_pos_mock

        # When
        with patch('mower.resources.services.mower_parsers_service.open',
                    mock_open(read_data=text_file_data), create=True) as file_mock:
            file_mock.return_value.__iter__.return_value = text_file_data.splitlines()
            mowers, lawn = parser.parse()

        # Then
        expected_mowers = {0: MagicMock(position='2 2 N\n', directions='LBFR\nL\nF\nRRRLLBB\n'),
                           1: MagicMock(position='3 3 E\n', directions='RRR\n'),
                           2: MagicMock(position='5 5 S')}
        expected_lawn = MagicMock(height_width='4 4\n')

        self.assertEquals(expected_lawn.height_width, lawn.height_width)

        for index, mower in expected_mowers.items():
            self.assertEquals(mower.position, mowers[index].position)
            if len(mowers[index].directions) != 0:
                self.assertEquals(mower.directions, mowers[index].directions)
            else:
                self.assertEqual(0, len(mowers[index].directions))

    def test_parse_raises_on_wrong_file_info(self):
        """Test parse mower raises error on wrong mower file data."""
        # Given
        parser = FileMowerParserService('filename')
        text_file_data = '\n'.join(['4 4', '2 2', 'LBFR', 'L', 'F', 'RRRLLBB'])
        lawn_mock.from_str = lawn_from_str
        mower_mock.extend_directions_from_str = mower_extend_dir_mock
        mower_mock.from_initial_position_str = mower_from_init_pos_mock

        # When
        with patch('mower.resources.services.mower_parsers_service.open',
                    mock_open(read_data=text_file_data), create=True) as file_mock:
            file_mock.return_value.__iter__.return_value = text_file_data.splitlines()
            self.assertRaises(LoadFileParserError, parser.parse)
