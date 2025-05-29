import abc
from typing import Any, Union


class BaseReader(abc.ABC):
    """
    Abstract base class for all readers.
    """

    @abc.abstractmethod
    def process(self, *args, **kwargs) -> Union[Any]:
        """
        Abstract method for reading input with flexible arguments.

        Args:
            *args: Positional arguments (implementation-defined).
            **kwargs: Keyword arguments (implementation-defined).

        Returns:
            dict: The parsed result.
        """
        pass
