import abc
from typing import Any, Union


class BaseReader(abc.ABC):
    """
    Abstract base class for all readers.
    """

    def __init__(self, path: str):
        """
        Initialize the Reader class.
        Args:
            path (str): The path to the file to be read.
        """
        self.data = self._read(path)

    @abc.abstractmethod
    def _read(self, *args, **kwargs) -> Union[Any]:
        """
        Abstract method for reading input with flexible arguments.

        Args:
            *args: Positional arguments (implementation-defined).
            **kwargs: Keyword arguments (implementation-defined).

        Returns:
            dict: The parsed result.
        """
        pass
