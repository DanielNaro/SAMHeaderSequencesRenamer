from typing import Dict, Set, TextIO

from utils import read_translations, read_available_sequences


class SamHeaderSequencesRenamerUtils:
    @staticmethod
    def get_non_available_sequences(translations: Dict[str, str], available_sequences: Set[str]) -> Set[str]:
        non_available_sequences: Set[str] = set()
        for translated_to in translations.values():
            if translated_to not in available_sequences:
                non_available_sequences.add(translated_to)
        return non_available_sequences

    @staticmethod
    def get_non_available_sequences_from_path(
            translation_file_path: str,
            available_sequences_file_path: str
    ) -> Set[str]:
        translations = read_translations(translation_file_path)
        available_sequences = read_available_sequences(available_sequences_file_path)
        return SamHeaderSequencesRenamerUtils.get_non_available_sequences(translations, available_sequences)

    @staticmethod
    def get_translation(sequence_name: str, translations: Dict[str, str]) -> str:
        if sequence_name in translations:
            return translations[sequence_name]
        else:
            return sequence_name

    @staticmethod
    def get_line_translation(line: str, translations: Dict[str, str]) -> str:
        if not line.startswith('@SQ'):
            return line
        elements = line.split()
        for i in range(len(elements)):
            element = elements[i]
            if element.startswith("SN:"):
                elements[i] = "SN:" + SamHeaderSequencesRenamerUtils.get_translation(elements[i][3:], translations)
        return '\t'.join(elements) + '\n'

    @staticmethod
    def get_header_translation(file_input: TextIO, file_output: TextIO, translations: Dict[str, str]):
        for line in file_input:
            file_output.write(SamHeaderSequencesRenamerUtils.get_line_translation(line, translations))
