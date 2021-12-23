from typing import Dict, Set


def read_translations(file_path: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    with open(file_path) as file_input:
        for line in file_input:
            [key, value] = line.strip().split()
            result[key] = value
    return result


def read_available_sequences(file_path: str) -> Set[str]:
    result: Set[str] = set()
    with open(file_path) as file_input:
        for line in file_input:
            result.add(line.strip())
    return result
