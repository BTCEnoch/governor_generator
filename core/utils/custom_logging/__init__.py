"""
Custom Logging Package

This package provides standardized logging configuration for:
- Console output
- File logging
- Structured log formats
- Log level management
"""

from .custom_logger import setup_logger

__all__ = ['setup_logger'] 
