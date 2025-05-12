"""Text Processing Utility Functions"""


import io

from typing import Iterable, List, Union


__all__: List[str] = [
    'strip_discard_empty_lines',
]


LineProvider = Union[Iterable[str], io.TextIOWrapper]


def strip_discard_empty_lines(lines: LineProvider) -> List[str]:
    """Sanitizes string lines in an iterable such that:

    * Leading and trailing whitespace is discarded ("strip()")
    * Empty lines (including whitespace-only) are discarded

    :param lines: An iterable of string lines to process
    :type lines: Iterable[str]

    :return: The list of normalized (non-empty) strings.
    :rtype: List[str]
    """
    return list(
        [
            line.strip()
            for line in lines
            if line.strip()
        ]
    )
