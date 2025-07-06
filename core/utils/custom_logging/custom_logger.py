"""
Logging Utilities
Standardized logging configuration for the Governor Generation system
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union
from datetime import datetime

def setup_logger(
    name: str,
    log_file: Optional[Union[str, Path]] = None,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    file_mode: str = 'a'
) -> logging.Logger:
    """
    Set up a logger with console and optional file output
    
    Args:
        name: Logger name
        log_file: Optional path to log file
        level: Logging level
        format_string: Optional custom format string
        file_mode: File open mode ('a' for append, 'w' for write)
    
    Returns:
        Configured logger instance
        
    Raises:
        ValueError: If log_file is provided but its parent directory does not exist
    """
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Configure logger
    logger.setLevel(level)
    logger.propagate = False  # Prevent double logging
    
    # Use custom or default format
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_string)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        # Convert to Path if string
        if isinstance(log_file, str):
            log_file = Path(log_file)
            
        # Validate parent directory exists
        try:
            # Check if path is absolute and exists
            if log_file.is_absolute() and not log_file.parent.exists():
                raise ValueError(f"Log directory does not exist: {log_file.parent}")
            
            # Try to resolve relative path
            resolved_path = log_file.resolve()
            if not resolved_path.parent.exists():
                raise ValueError(f"Log directory does not exist: {resolved_path.parent}")
        except (RuntimeError, OSError) as e:
            # Handle invalid paths (e.g. too long, invalid characters)
            raise ValueError(f"Invalid log file path: {log_file}") from e
        
        file_handler = logging.FileHandler(str(log_file), mode=file_mode)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_batch_logger(batch_id: str, base_dir: Optional[Union[str, Path]] = None, log_file: Optional[Union[str, Path]] = None) -> logging.Logger:
    """
    Get a logger configured for batch processing
    
    Args:
        batch_id: Unique batch identifier
        base_dir: Optional base directory for log files
        log_file: Optional specific log file path (overrides base_dir)
    
    Returns:
        Logger configured for batch processing
    """
    # Use provided log file or generate one in base_dir
    if log_file is None and base_dir is not None:
        # Set up log directory
        if isinstance(base_dir, str):
            base_dir = Path(base_dir)
        
        # Create timestamp-based log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = base_dir / f"batch_{batch_id}_{timestamp}.log"
    
    # Configure logger
    logger = setup_logger(
        name=f"batch_{batch_id}",
        log_file=log_file,
        format_string='%(asctime)s - %(levelname)s - [%(name)s] %(message)s'
    )
    
    return logger

def get_mystical_logger(system_name: str, base_dir: Optional[Union[str, Path]] = None, log_file: Optional[Union[str, Path]] = None) -> logging.Logger:
    """
    Get a logger configured for mystical system operations
    
    Args:
        system_name: Name of the mystical system
        base_dir: Optional base directory for log files
        log_file: Optional specific log file path (overrides base_dir)
    
    Returns:
        Logger configured for mystical system operations
    """
    # Use provided log file or generate one in base_dir
    if log_file is None and base_dir is not None:
        # Set up log directory
        if isinstance(base_dir, str):
            base_dir = Path(base_dir)
        
        # Create log file
        log_file = base_dir / f"{system_name}.log"
    
    # Configure logger
    logger = setup_logger(
        name=f"mystical_{system_name}",
        log_file=log_file,
        format_string='%(asctime)s - %(levelname)s - [%(name)s] %(message)s'
    )
    
    return logger

def get_governor_logger(governor_id: str, base_dir: Optional[Union[str, Path]] = None, log_file: Optional[Union[str, Path]] = None) -> logging.Logger:
    """
    Get a logger configured for governor operations
    
    Args:
        governor_id: Unique governor identifier
        base_dir: Optional base directory for log files
        log_file: Optional specific log file path (overrides base_dir)
    
    Returns:
        Logger configured for governor operations
    """
    # Use provided log file or generate one in base_dir
    if log_file is None and base_dir is not None:
        # Set up log directory
        if isinstance(base_dir, str):
            base_dir = Path(base_dir)
        
        # Create log file
        log_file = base_dir / f"governor_{governor_id}.log"
    
    # Configure logger
    logger = setup_logger(
        name=f"governor_{governor_id}",
        log_file=log_file,
        format_string='%(asctime)s - %(levelname)s - [%(name)s] %(message)s'
    )
    
    return logger 
