from typing import Set
from unittest import TestCase

from SamHeaderSequencesRenamerUtils import SamHeaderSequencesRenamerUtils
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
            "chr2",
            SamHeaderSequencesRenamerUtils.get_translation(
                '2',
                {'2': 'chr2'}
            )
        )
        self.assertEqual(
            "22",
            SamHeaderSequencesRenamerUtils.get_translation(
                '22',
                {'2': 'chr2'}
            )
        )

    def test_get_line_translation(self):
        line = "@HD	VN:1.5	SO:coordinate\n"
        self.assertEqual(line, SamHeaderSequencesRenamerUtils.get_line_translation(line, {'2': 'chr2'}))

        line_sq = "@SQ	SN:2	LN:243199373\n"
        expected_line_sq = "@SQ	SN:chr2	LN:243199373\n"
        self.assertEqual(expected_line_sq, SamHeaderSequencesRenamerUtils.get_line_translation(line_sq, {'2': 'chr2'}))

    def test_get_header_translation(self):
        translations = read_translations("TestMaterial/test_translations.txt")
        test_output = 'TestOutputs/header_translation_check.txt'
        with open('TestMaterial/header.txt') as input_file, \
                open(test_output, 'w') as output_file:
            SamHeaderSequencesRenamerUtils.get_header_translation(input_file, output_file, translations)

        with open(test_output) as result_file, \
                open('TestMaterial/expected_translated_header.txt') as expected_file:
            result = result_file.read()
            expected = expected_file.read()
            self.assertEqual(expected, result)
