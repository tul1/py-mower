import pytest

from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open, call

from mower.resources.services.mower_parsers_service import FileMowerParserService
from mower.utils.exceptions import LoadFileParserError


@patch('mower.resources.services.mower_parsers_service.MowerModel')
class TestParseMower(TestCase):
    """Mower Parser test."""
    def test_parse_mower_position_raises_on_mower_outside_lawn(self, mwr_mock):
        """Test parse mower raises error on wrong mower file data."""
        # Given
        mowers = dict()
        lawn = MagicMock(height=2, width=2)

        # When / Then
        with self.assertRaises(LoadFileParserError):
            mwr_mock.position_from_str.return_value = (4, 2, 'N')
            FileMowerParserService.parse_mower_position(mowers, lawn, 'line')

        with self.assertRaises(LoadFileParserError):
            mwr_mock.position_from_str.return_value = (0, 4, 'N')
            FileMowerParserService.parse_mower_position(mowers, lawn, 'line')

        with self.assertRaises(LoadFileParserError):
            mwr_mock.position_from_str.return_value = (4, 0, 'N')
            FileMowerParserService.parse_mower_position(mowers, lawn, 'line')

        with self.assertRaises(LoadFileParserError):
            mwr_mock.position_from_str.return_value = (2, 4, 'N')
            FileMowerParserService.parse_mower_position(mowers, lawn, 'line')

    def test_parse_mower_raises_on_two_mowers_in_the_position(self, mwr_mock):
        """Test parse mower raises error on wrong mower file data."""
        # Given
        mowers = {(2, 4): (2, 4, 'S')}
        lawn = MagicMock(height=4, width=4)
        mwr_mock.position_from_str.return_value = (2, 4, 'N')

        # When / Then
        with self.assertRaises(LoadFileParserError):
            FileMowerParserService.parse_mower_position(mowers, lawn, 'line')

    def test_parse_mower(self, mwr_mock):
        """Test parse mower raises error on wrong mower file data."""
        # Given
        mowers = {(2, 4): (2, 4, 'S')}
        lawn = MagicMock(height=4, width=4)
        mwr_mock.position_from_str.return_value = (2, 2, 'N')

        # When
        mwr_pos, mwrs = FileMowerParserService.parse_mower_position(mowers, lawn, 'line')

        # Then
        expected_mowers = {(2, 4): (2, 4, 'S'), (2, 2): mwr_mock.return_value}

        self.assertEquals(expected_mowers, mwrs)
        self.assertEquals((2, 2), mwr_pos)


@patch('mower.resources.services.mower_parsers_service.MowerModel.extend_directions_from_str')
class TestParseDirections(TestCase):
    """Mower Directions Parser test."""
    def test_parse_mower_directions(self, extend_dirs_mock):
        """Test parse mower raises error on wrong directions."""
        # Given
        mowers = {(1, 1): 'mower data'}

        # When
        actual_mowers = FileMowerParserService.parse_mower_directions(mowers, (1, 1), 'line')

        # Then
        expected_mowers = {(1, 1): extend_dirs_mock.return_value}

        self.assertEquals(expected_mowers, actual_mowers)

    def test_parse_mower_directions_raises_on_nonunexistent_posxy(self, _):
        """Test parse mower raises error on wrong directions."""
        # Given
        mowers = dict()

        # When / Then
        with self.assertRaises(LoadFileParserError):
            FileMowerParserService.parse_mower_directions(mowers, (1, 1), 'line')


def patch_and_run_parse_method(method_input):
    """Helper function patch parser method."""
    parser = FileMowerParserService('filename')
    with patch('mower.resources.services.mower_parsers_service.open',
               mock_open(read_data=method_input), create=True) as file_mock:
        file_mock.return_value.__iter__.return_value = method_input.splitlines()
        return parser.parse()


def assert_parse_method_raises_custom_exception(method_input, expected_exception, assert_method):
    """Helper function to assert specific exception for parser method."""
    text_file_data = '\n'.join(method_input)
    with assert_method(expected_exception):
        patch_and_run_parse_method(text_file_data)


@patch('mower.resources.services.mower_parsers_service.FileMowerParserService.parse_mower_directions')
@patch('mower.resources.services.mower_parsers_service.FileMowerParserService.parse_mower_position')
@patch('mower.resources.services.mower_parsers_service.FileMowerParserService.parse_lawn')
class TestFileMowerParserService(TestCase):
    """FileMower Parser Service test."""
    def test_parse_empty_file(self, _, __, ___):
        """Test parse a mower file."""
        assert_parse_method_raises_custom_exception(method_input=['  '],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_with_no_lawn_params_nor_init_mower_pos(self, _, __, ___):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['LBFR', 'L', 'F', 'RRRLLBB'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_on_with_no_lawn_params(self, _, __, ___):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_on_single_mower_with_two_lawn_params(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['4 4', '4 4'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_on_single_mower_with_wrong_mower_coord(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['4 4', '2 2 NN'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

        assert_parse_method_raises_custom_exception(method_input=['4 4', '2 N'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

        assert_parse_method_raises_custom_exception(method_input=['4 4', 'e 2 N'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

        assert_parse_method_raises_custom_exception(method_input=['4 4', '2 e N'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

        assert_parse_method_raises_custom_exception(method_input=['4 4', '2 2 N 3'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

        assert_parse_method_raises_custom_exception(method_input=['4 4', '2 2 N LR'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

        assert_parse_method_raises_custom_exception(method_input=['4 4', '2 2 R'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_raises_on_single_mower_with_random_input(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse mower raises error on wrong mower file data."""
        assert_parse_method_raises_custom_exception(method_input=['dsfdsfsdfsdf'],
                                                    expected_exception=LoadFileParserError,
                                                    assert_method=self.assertRaises)

    def test_parse_file_with_no_mower(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse a mower file."""
        # Given / When
        patch_and_run_parse_method('\n'.join(['4 4']))

        # Then
        lawn_mock.assert_called_once_with('4 4')
        mwr_pos_mock.assert_not_called()
        mwr_dirs_mock.assert_not_called()

    def test_parse_file_with_single_mower(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse a mower file."""
        # Given
        mwr_pos_mock.return_value = ((2, 2), MagicMock())

        # When
        patch_and_run_parse_method('\n'.join(['4 4', '2 2 N', 'LBFR']))

        # Then
        lawn_mock.assert_called_once_with('4 4\n')
        mwr_pos_mock.assert_called_once_with(dict(), lawn_mock.return_value, '2 2 N\n')
        mwr_dirs_mock.assert_called_once_with(mwr_pos_mock.return_value[1], (2, 2), 'LBFR')

    def test_parse_file_with_multiplemowers_mower_with_no_directions(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse a mower file."""
        # Given
        mwr_pos_mock.return_value = ((2, 2), MagicMock())

        # When
        patch_and_run_parse_method('\n'.join(['4 4', '1 2 E', '2 3 S', '4 4 N', '1 1 W']))

        # Then
        lawn_mock.assert_called_once_with('4 4\n')

        mwr_pos_calls = [call(dict(), lawn_mock.return_value, '1 2 E\n'),
                         call(mwr_pos_mock.return_value[1], lawn_mock.return_value, '2 3 S\n'),
                         call(mwr_pos_mock.return_value[1], lawn_mock.return_value, '4 4 N\n'),
                         call(mwr_pos_mock.return_value[1], lawn_mock.return_value, '1 1 W')]
        mwr_pos_mock.assert_has_calls(mwr_pos_calls)

        mwr_dirs_mock.assert_not_called()

    def test_parse_file_with_single_mower_with_multiline_directions(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse a mower file with multiple line directions."""
        # Given
        mwr_pos_mock.return_value = ((2, 2), MagicMock())

        # When
        patch_and_run_parse_method('\n'.join(['4 4', '2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB']))

        # Then
        lawn_mock.assert_called_once_with('4 4\n')
        mwr_pos_mock.assert_called_once_with(dict(), lawn_mock.return_value, '2 2 N\n')

        mwr_dir_calls = [call(mwr_pos_mock.return_value[1], (2, 2), 'LBFR\n'),
                         call(mwr_dirs_mock.return_value, (2, 2), 'L\n'),
                         call(mwr_dirs_mock.return_value, (2, 2), 'F\n'),
                         call(mwr_dirs_mock.return_value, (2, 2), 'RRRLLBB')]
        mwr_dirs_mock.assert_has_calls(mwr_dir_calls)

    def test_parse_file_with_multiple_mowers_with_multiline_directions(self, lawn_mock, mwr_pos_mock, mwr_dirs_mock):
        """Test parse a mower file with multiple line directions."""
        # Given
        mowers = MagicMock()
        mwr_pos_mock.side_effect = [((2, 2), mowers), ((3, 3), mowers), ((5, 5), mowers)]

        # When
        patch_and_run_parse_method('\n'.join(['4 4', '2 2 N', 'LBFR', 'L', 'F', 'RRRLLBB', '3 3 E', 'RRR', '5 5 S']))

        # Then
        lawn_mock.assert_called_once_with('4 4\n')

        mwr_pos_calls = [call(dict(), lawn_mock.return_value, '2 2 N\n'),
                         call(mwr_dirs_mock.return_value, lawn_mock.return_value, '3 3 E\n'),
                         call(mwr_dirs_mock.return_value, lawn_mock.return_value, '5 5 S')]
        mwr_pos_mock.assert_has_calls(mwr_pos_calls)

        mwr_dirs_calls = [call(mowers, (2, 2), 'LBFR\n'),
                          call(mwr_dirs_mock.return_value, (2, 2), 'L\n'),
                          call(mwr_dirs_mock.return_value, (2, 2), 'F\n'),
                          call(mwr_dirs_mock.return_value, (2, 2), 'RRRLLBB\n'),
                          call(mowers, (3, 3), 'RRR\n')]
        mwr_dirs_mock.assert_has_calls(mwr_dirs_calls)
