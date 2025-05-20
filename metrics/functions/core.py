import abc


class BaseMetric(abc.ABC):
    """
    Abstract base class for all metrics.

    This class defines the interface for calculating metrics.
    Subclasses should implement the `calculate` method to provide specific metric calculation logic.
    """

    @abc.abstractmethod
    def calculate(self, *args, **kwargs) -> float:
        """
        Abstract method for calculating a metric.

        Args:
            *args: Positional arguments (implementation-defined).
            **kwargs: Keyword arguments (implementation-defined).

        Returns:
            float: The calculated metric value.
        """
        pass
