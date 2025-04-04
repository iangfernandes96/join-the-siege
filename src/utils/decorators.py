import logging
import functools
from typing import Callable, Any
from ..models import ClassifierResult

logger = logging.getLogger(__name__)


def handle_classifier_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to handle classifier errors consistently.

    Args:
        func: The classifier method to wrap

    Returns:
        Wrapped function with standardized error handling
    """

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs) -> ClassifierResult:
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {str(e)}")
            return ClassifierResult(classifier_name=self.__class__.__name__)

    return wrapper
