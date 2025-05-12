import requests
from . import get_file_name_from_url as get_file_name_from_url, get_qs_value as get_qs_value, split_url as split_url
from ..errors import M3U8Error as M3U8Error
from ..fileio.ffmpeg import run_ffmpeg as run_ffmpeg
from ..textio import print_error as print_error, print_warning as print_warning
from m3u8 import M3U8
from pathlib import Path
from rich.progress import Progress
from typing import Any

def get_m3u8_cookies(m3u8_url: str) -> dict[str, Any]: ...
def get_m3u8_progress(disable_loading_bar: bool) -> Progress: ...
def fetch_m3u8_segment_playlist(m3u8_url: str, cookies: dict[str, str] | None = None, session: requests.Session | None = None, recursion_depth: int = 0) -> M3U8: ...
def download_m3u8(m3u8_url: str, save_path: Path, session: requests.Session | None = None) -> Path: ...
