import sys
from typing import Dict, Set, TextIO, Tuple, Optional

from utils import read_translations, read_available_sequences, simplify_translation_info


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
        return SamHeaderSequencesRenamerUtils.get_non_available_sequences(
            simplify_translation_info(translations), available_sequences)

    @staticmethod
    def get_translation(
            sequence_name: str,
            translations: Dict[str, Tuple[str, Optional[int]]]
    ) -> Tuple[str, Optional[int], bool]:
        if sequence_name in translations:
            return translations[sequence_name][0], translations[sequence_name][1], True
        else:
            return sequence_name, None, False

    @staticmethod
    def get_line_translation(
            line: str,
            translations: Dict[str, Tuple[str, Optional[int]]],
            keep: bool = False
    ) -> Tuple[str, Optional[str]]:
        if not line.startswith('@SQ'):
            return line, None
        elements = line.split()
        new_sequence_name = None

        for i in range(len(elements)):
            element = elements[i]

            if element.startswith("SN:"):
                new_sequence_name, length, trustworthy = SamHeaderSequencesRenamerUtils.get_translation(elements[i][3:],
                                                                                                        translations)
                if not trustworthy:
                    if not keep:
                        return '', None
                elements[i] = "SN:" + new_sequence_name

        if new_sequence_name is None:
            print("line \"" + line + "\" is missing sequence name", file=sys.stderr)
            exit(2)

        if length is not None:
            for i in range(len(elements)):
                element = elements[i]
                if element.startswith("LN:"):
                    elements[i] = "LN:" + str(length)

        return '\t'.join(elements) + '\n', new_sequence_name

    @staticmethod
    def get_header_translation(
            file_input: TextIO,
            file_output: TextIO,
            translations: Dict[str, Tuple[str, Optional[int]]],
            to_keep_file: Optional[TextIO] = None,
            keep_untrustworthy_translations: bool = False):
        to_keep = []
        for line in file_input:
            new_line, optional_sequence_to_keep = SamHeaderSequencesRenamerUtils.get_line_translation(
                line,
                translations,
                keep_untrustworthy_translations
            )
            file_output.write(new_line)
            if optional_sequence_to_keep is not None:
                to_keep.append(optional_sequence_to_keep)
        if to_keep_file is not None:
            to_keep_file.write(' '.join(to_keep))
