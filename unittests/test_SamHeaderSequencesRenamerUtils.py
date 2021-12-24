from typing import Set
from unittest import TestCase

from SamHeaderSequencesRenamerUtils import SamHeaderSequencesRenamerUtils
from unittests.capture_output import captured_output
from utils import read_translations


class TestSamHeaderSequencesRenamer(TestCase):
    def test_get_non_available_sequences(self):
        test_dict = {
            '1': 'chr1',
            '2': '2'
        }
        available_sequences = {'chr1', 'chr2', 'chr3'}
        result: Set[str] = SamHeaderSequencesRenamerUtils.get_non_available_sequences(test_dict, available_sequences)
        self.assertSetEqual({'2'}, result)

    def test_get_non_available_sequences_from_path(self):
        result: Set[str] = SamHeaderSequencesRenamerUtils.get_non_available_sequences_from_path(
            'TestMaterial/test_translations.txt',
            'TestMaterial/test_available_sequences.txt'
        )
        self.assertSetEqual({'2'}, result)

    def test_get_translation(self):
        self.assertEqual(
            ("chr2", True),
            SamHeaderSequencesRenamerUtils.get_translation(
                '2',
                {'2': 'chr2'}
            )
        )
        self.assertEqual(
            ("22", False),
            SamHeaderSequencesRenamerUtils.get_translation(
                '22',
                {'2': 'chr2'}
            )
        )

    def test_get_line_translation(self):
        line = "@HD	VN:1.5	SO:coordinate\n"
        self.assertEqual((line, None), SamHeaderSequencesRenamerUtils.get_line_translation(line, {'2': 'chr2'}))

        line_sq = "@SQ	SN:2	LN:243199373\n"
        expected_line_sq = "@SQ	SN:chr2	LN:243199373\n"
        self.assertEqual((expected_line_sq, 'chr2'),
                         SamHeaderSequencesRenamerUtils.get_line_translation(line_sq, {'2': 'chr2'}))

    def test_get_header_translation(self):
        translations = read_translations("TestMaterial/test_translations.txt")
        test_output = 'TestOutputs/header_translation_check.txt'
        to_keep = 'TestOutputs/to_keep.txt'
        with open('TestMaterial/header.txt') as input_file, \
                open(test_output, 'w') as output_file, \
                open(to_keep, 'w') as to_keep_file:
            SamHeaderSequencesRenamerUtils.get_header_translation(input_file, output_file, translations, to_keep_file)

        with open(test_output) as result_file, \
                open('TestMaterial/expected_translated_header.txt') as expected_file:
            result = result_file.read()
            expected = expected_file.read()
            self.assertEqual(expected, result)

        with open(to_keep) as result_file, \
                open('TestMaterial/expected_to_keep.txt') as expected_file:
            result = result_file.read()
            expected = expected_file.read()
            self.assertEqual(expected, result)

    def test_sequence_line_without_name(self):
        sequence_line = "@SQ	LN:35477943"
        with self.assertRaises(SystemExit) as cm:
            with captured_output() as (out, err):
                SamHeaderSequencesRenamerUtils.get_line_translation(
                    sequence_line,
                    {}
                )
        self.assertEqual(cm.exception.code, 2)

        result = err.getvalue().strip()
        expected = "line \"" + sequence_line + "\" is missing sequence name"
        self.assertEqual(expected, result)
