"""Code Timing Class by RealPython

This is based on https://realpython.com/python-timer/ with
minor modifications.
"""

#region Imports

import time

from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Dict, List, Optional

#endregion

#region Exports

__all__: List[str] = [
    'Timer',
    'TimerError',
]

#endregion

#region Classes

class TimerError(Exception):
    """A custom exception type used to report errors within the Timer class.
    """



@dataclass
class Timer(ContextDecorator):
    """Times your code using a class, context manager, or decorator.
    
    :param name: Only required when using multiple timers in parallel.
    :type name: str

    :param text: Format string for the result message when a timer stops.
    :type text: str

    :param logger: You could set this to `print`. The callback function
        to receive the result message when a timer stops.
    :type logger: Callable[[str], None]
    
    To summarize, you can use `Timer` in three different ways:

    As a class::

        t = Timer(name="class")
        t.start()
        # Do something
        t.stop()

    As a context manager::

        with Timer(name="context manager"):
            # Do something

    As a decorator::

        @Timer(name="decorator")
        def stuff():
            # Do something

    This kind of Python timer is mainly useful for monitoring the time
    that your code spends at individual key code blocks or functions.
    """

    _start_time: Optional[float] = field(default=None, init=False, repr=False)
    """Internal variable for the start time"""

    name: Optional[str] = None
    """Name of the timer when using multiple timers"""

    logger: Optional[Callable[[str], None]] = None
    """The callback function receiving the result message"""

    text: str = "Elapsed time: {:0.4f} seconds"
    """The format string for the result message"""

    timers: ClassVar[Dict[str, float]] = {}
    """A class dictionary of named timers that can run in parallel"""


    def __post_init__(self) -> None:
        """Initialization: Adds timer to `timers` dictionary."""
        if self.name:
            self.timers.setdefault(self.name, 0)


    def start(self) -> None:
        """Starts a new timer."""
        if self._start_time is not None:
            raise TimerError(f"Timer is already running. Use .stop() to stop it.")

        self._start_time = time.perf_counter()


    def stop(self) -> float:
        """Stops the timer and reports the elapsed time."""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it.")

        # Calculate elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.logger:
            self.logger(self.text.format(elapsed_time))

        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time


    def __enter__(self) -> "Timer":
        """Starts a new timer as a context manager."""
        self.start()
        return self


    def __exit__(self, *exc_info: Any) -> None:
        """Stops the context manager timer."""
        self.stop()

#endregion
