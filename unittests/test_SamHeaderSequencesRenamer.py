import sys
from unittest import TestCase

from Main import SamHeaderSequencesRenamer
from unittests.capture_output import captured_output


class TestMain(TestCase):
    def test_check_availability_sequences_with_output(self):
        sys.argv = [
            'samHeaderSequencesRenamer',
            'check_availability_sequences',
            '-t',
            'TestMaterial/test_translations.txt',
            '-a',
            'TestMaterial/test_available_sequences.txt',
            '-o',
            'TestOutputs/main_availability_check.txt'
        ]
        SamHeaderSequencesRenamer()

        with open('TestOutputs/main_availability_check.txt') as result_file, \
                open('TestMaterial/expected_main_availability_check.txt') as expected_file:
            result = result_file.read()
            expected = expected_file.read()

            self.assertEqual(expected, result)

    def test_check_availability_empty(self):
        sys.argv = [
            'samHeaderSequencesRenamer',
            'check_availability_sequences'
        ]
        with self.assertRaises(SystemExit) as cm:
            with captured_output() as (out, err):
                SamHeaderSequencesRenamer()
        self.assertEqual(cm.exception.code, 2)

        with open('TestMaterial/expected_main_availability_empty_response.txt') as expected_file:
            result = err.getvalue().strip()
            expected = expected_file.read()

            if result == expected:
                return

            with open('TestMaterial/expected_main_availability_empty_response_variant2.txt') as expected_file_variant2:
                expected_variant = expected_file_variant2.read()
                self.assertEqual(expected_variant, result)

    def test_check_availability_sequences(self):
        sys.argv = [
            'samHeaderSequencesRenamer',
            'check_availability_sequences',
            '-t',
            'TestMaterial/test_translations.txt',
            '-a',
            'TestMaterial/test_available_sequences.txt'
        ]
        with captured_output() as (out, err):
            SamHeaderSequencesRenamer()

        with open('TestMaterial/expected_main_availability_check.txt') as expected_file:
            result = out.getvalue().strip()
            expected = expected_file.read()
            self.assertEqual(expected, result)

    def test_check_translate(self):
        sys.argv = [
            'samHeaderSequencesRenamer',
            'translate',
            '-t',
            'TestMaterial/test_translations.txt',
            '-i',
            'TestMaterial/header.txt',
            '-o',
            'TestOutputs/header_command_translation.txt'
        ]
        SamHeaderSequencesRenamer()

        with open('TestOutputs/header_command_translation.txt') as result, \
                open('TestMaterial/expected_translated_header.txt') as expected_file:
            result = result.read()
            expected = expected_file.read()
            self.assertEqual(expected, result)

    def test_check_empty(self):
        sys.argv = [
            'samHeaderSequencesRenamer'
        ]
        with self.assertRaises(SystemExit) as cm:
            with captured_output() as (out, err):
                SamHeaderSequencesRenamer()
        self.assertEqual(cm.exception.code, 2)

        with open('TestMaterial/expected_main_empty_response.txt') as expected_file:
            result = err.getvalue().strip()
            expected = expected_file.read()
            self.assertEqual(expected, result)

    def test_unknown_command(self):
        sys.argv = [
            'samHeaderSequencesRenamer',
            'test'
        ]
        with self.assertRaises(SystemExit) as cm:
            with captured_output() as (out, err):
                SamHeaderSequencesRenamer()
        self.assertEqual(cm.exception.code, 1)

        with open('TestMaterial/expected_main_wrong_command.txt') as expected_file:
            result = out.getvalue().strip()
            expected = expected_file.read()
            if expected == result:
                return
            else:
                with open('TestMaterial/expected_main_wrong_command_variant.txt') as expected_file_variant:
                    self.assertEqual(expected_file_variant.read(), result)
