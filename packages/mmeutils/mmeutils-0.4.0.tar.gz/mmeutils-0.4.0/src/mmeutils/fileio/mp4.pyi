import _hashlib
from _typeshed import Incomplete
from io import BufferedReader
from pathlib import Path
from typing import Callable, Iterable

__all__ = ['MP4Box', 'hash_mp4file', 'get_boxes', 'hash_mp4box']

class MP4Box:
    position: Incomplete
    size: Incomplete
    fourcc: Incomplete
    def __init__(self, size_bytes: bytes, fourcc_bytes: bytes, position: int) -> None: ...
    @staticmethod
    def convert_to_fourcc(fourcc_bytes: bytes) -> str: ...

def get_boxes(reader: BufferedReader) -> Iterable[MP4Box]: ...
def hash_mp4box(algorithm: _hashlib.HASH, reader: BufferedReader, box: MP4Box) -> None: ...
def hash_mp4file(algorithm, file_name: str | Path, print: Callable | None = None, use_broken_algo: bool = False) -> str: ...
