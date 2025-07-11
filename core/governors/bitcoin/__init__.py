"""
Bitcoin Integration

Handles Bitcoin-related functionality including ordinal inscriptions
and state management.
"""

from .ordinals import OrdinalHandler
from .state import BitcoinState
from .schemas import (
    Inscription,
    InscriptionContent,
    InscriptionMetadata,
    StateTransition,
    BitcoinBlock,
    StateProof
)

__all__ = [
    'OrdinalHandler',
    'BitcoinState',
    'Inscription',
    'InscriptionContent',
    'InscriptionMetadata',
    'StateTransition',
    'BitcoinBlock',
    'StateProof'
] 