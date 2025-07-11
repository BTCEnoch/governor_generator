"""
Error Handling Utilities
Common error handling and reporting functions
"""

import logging
import traceback
from typing import Any, Dict, List, Optional, Type, TypeVar, Callable
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')

def safe_execute(func: Callable[..., T], *args, **kwargs) -> Optional[T]:
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Function result or None if error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {e}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        return None

def retry_on_error(
    max_retries: int = 3,
    retry_exceptions: Optional[List[Type[Exception]]] = None,
    delay: float = 0
) -> Callable:
    """
    Decorator to retry function on error
    
    Args:
        max_retries: Maximum number of retries (default: 3)
        retry_exceptions: List of exceptions to retry on (default: all)
        delay: Delay between retries in seconds (default: 0)
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            exceptions = retry_exceptions or [Exception]
            last_error = Exception("No error occurred")  # Default error
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as e:
                    last_error = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {e}"
                    )
                    if attempt < max_retries - 1 and delay:
                        time.sleep(delay)
                        
            logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            raise last_error
            
        return wrapper
    return decorator

def format_error(error: Exception) -> Dict[str, Any]:
    """
    Format exception info into a dictionary
    
    Args:
        error: Exception to format
        
    Returns:
        Dictionary with error details
    """
    return {
        'type': error.__class__.__name__,
        'message': str(error),
        'traceback': traceback.format_exc()
    }

def handle_errors(
    default_value: Any = None,
    log_level: int = logging.ERROR,
    reraise: bool = False
) -> Callable:
    """
    Decorator for standardized error handling
    
    Args:
        default_value: Value to return on error
        log_level: Logging level for errors
        reraise: Whether to reraise caught exceptions
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(log_level, f"Error in {func.__name__}: {e}")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                
                if reraise:
                    raise
                    
                return default_value
                
        return wrapper
    return decorator

"""
Common error classes for the Governor Generation system.
"""

class BatchProcessingError(Exception):
    """Raised when a batch processing operation fails"""
    pass

class GovernorGenerationError(Exception):
    """Base class for Governor Generation system errors"""
    pass

class ValidationError(GovernorGenerationError):
    """Raised when data validation fails"""
    pass

class ProcessingError(GovernorGenerationError):
    """Raised when a processing operation fails"""
    pass

class ConfigurationError(GovernorGenerationError):
    """Raised when configuration is invalid"""
    pass

class ResourceNotFoundError(GovernorGenerationError):
    """Raised when a required resource is not found"""
    pass

class BitcoinIntegrationError(GovernorGenerationError):
    """Raised when Bitcoin integration fails"""
    pass 