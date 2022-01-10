from unittest import TestCase

from utils import read_translations, read_available_sequences, simplify_translation_info


class Test(TestCase):
    def test_read_translations(self):
        self.assertDictEqual(
            {'1': 'chr1', '2': '2'},
            simplify_translation_info(read_translations('TestMaterial/test_translations.txt'))
        )

    def test_read_available_sequences(self):
        self.assertSetEqual(
            {'chr1', 'chr2'},
            read_available_sequences('TestMaterial/test_available_sequences.txt')
        )
