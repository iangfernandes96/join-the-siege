import functools
from typing import Callable, Any
from ..models import ClassificationError
import logging

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
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return ClassificationError(
                error=f"Error in {func.__name__}: {str(e)}",
                details=str(e),
            )

    return wrapper
