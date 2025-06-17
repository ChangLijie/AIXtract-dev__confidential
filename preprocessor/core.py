import abc
from typing import Any, List, Tuple, Union


class BasePreprocessor(abc.ABC):
    """
    Abstract base class for all preprocessors.

    This class defines the interface for preprocessing data.
    Subclasses should implement the `preprocess` method to provide specific preprocessing logic.
    """

    @abc.abstractmethod
    def process(self, *args, **kwargs) -> Union[Any, Tuple[List[str], List[str]]]:
        """
        Abstract method for preprocessing data.

        Args:
            *args: Positional arguments (implementation-defined).
            **kwargs: Keyword arguments (implementation-defined).

        Returns:
            Any: The preprocessed data.
        """
        pass
