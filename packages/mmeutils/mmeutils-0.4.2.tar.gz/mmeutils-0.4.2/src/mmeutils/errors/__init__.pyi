__all__ = ['EXIT_ABORT', 'EXIT_ERROR', 'EXIT_SUCCESS', 'API_ERROR', 'CONFIG_ERROR', 'DOWNLOAD_ERROR', 'UNEXPECTED_ERROR', 'ApiError', 'ApiAuthenticationError', 'ConfigError', 'DownloadError', 'M3U8Error']

EXIT_SUCCESS: int
EXIT_ERROR: int
EXIT_ABORT: int
UNEXPECTED_ERROR: int
API_ERROR: int
CONFIG_ERROR: int
DOWNLOAD_ERROR: int

class ConfigError(RuntimeError):
    def __init__(self, *args) -> None: ...

class ApiError(RuntimeError):
    def __init__(self, *args) -> None: ...

class ApiAuthenticationError(ApiError):
    def __init__(self, *args) -> None: ...

class DownloadError(RuntimeError):
    def __init__(self, *args) -> None: ...

class M3U8Error(RuntimeError):
    def __init__(self, *args) -> None: ...
