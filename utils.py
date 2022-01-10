from typing import Dict, Set, Tuple, Optional, List


def simplify_translation_info(original_dict: Dict[str, Tuple[str, Optional[int]]]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for key, (translated_to, _) in original_dict.items():
        result[key] = translated_to
    return result


def read_translations(file_path: str) -> Dict[str, Tuple[str, Optional[int]]]:
    result: Dict[str, Tuple[str, Optional[int]]] = {}
    with open(file_path) as file_input:
        for line in file_input:
            elements: List[str] = line.strip().split()

            key = elements[0]
            value = elements[1]
            length = None
            if len(elements) == 3:
                length = int(elements[2])
            result[key] = (value, length)
    return result


def read_available_sequences(file_path: str) -> Set[str]:
    result: Set[str] = set()
    with open(file_path) as file_input:
        for line in file_input:
            result.add(line.strip())
    return result
