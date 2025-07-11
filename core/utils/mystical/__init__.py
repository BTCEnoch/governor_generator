"""
Mystical System Package

This package provides base classes and utilities for mystical systems:
- System configuration and validation
- Correspondence calculations
- Entity relationships
- Data formatting
- Bitcoin integration
"""

from .base import (
    ValidationResult,
    BitcoinMysticalSystem,
    MysticalAttribute,
    MysticalEntity
)
from .bitcoin_integration import BitcoinIntegration

__all__ = [
    'ValidationResult',
    'BitcoinMysticalSystem',
    'MysticalAttribute',
    'MysticalEntity',
    'BitcoinIntegration'
] 