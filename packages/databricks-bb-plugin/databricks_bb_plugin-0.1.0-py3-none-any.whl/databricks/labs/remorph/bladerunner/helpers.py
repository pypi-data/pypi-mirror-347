from lsprotocol.types import Range, Position


def full_range(source_code: str) -> Range:
    source_lines = source_code.split("\n")
    return Range(start=Position(0, 0), end=Position(len(source_lines), len(source_lines[-1])))
