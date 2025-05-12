import io
from typing import Iterable

__all__ = ['strip_discard_empty_lines']

LineProvider = Iterable[str] | io.TextIOWrapper

def strip_discard_empty_lines(lines: LineProvider) -> list[str]: ...
